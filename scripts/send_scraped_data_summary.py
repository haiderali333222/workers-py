import csv
import os
import sys
from datetime import datetime, timedelta

import pydash

from config.index import DB_NAME
from services.email.send_email import email_with_attachments
from services.mongo_db.connection import mongoConnection

# Import the necessary modules from the parent directory and its subdirectories
from services.slack.slack_message import send_detailed_slack_message
from utils.google_drive.upload_file import upload_to_google_drive

# facing import issues, We need to get parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
# Import the necessary modules from the parent directory and its subdirectories
from services.slack.slack_message import send_detailed_slack_message
from services.email.send_email import email_with_attachments

from services.mongo_db.connection import mongoConnection
from config.index import DB_NAME
from utils.google_drive.upload_file import upload_to_google_drive


db = mongoConnection()[DB_NAME]
JOB = "Scraped-Data-Summary"
SUBJECT = "Please find the sheet below"
RECEIVER = "ramzan@pursue.today"
CC = ["haider@pursue.today", "Ali@pursue.today", "amna.mubashar@pursue.today"]


def urls_code_data():
    status_summary = {}
    days_ago = timedelta(days=7)
    start_date = datetime.now() - days_ago

    pipeline = [
        {"$match": {"captured_at": {"$gte": start_date}}},
        {"$group": {"_id": {"competitor": "$competitor", "status": "$status"}, "count": {"$sum": 1}}},
    ]
    results = db.urls_status_code.aggregate(pipeline)
    for item in results:
        competitor = pydash.get(item, "_id.competitor")
        status = pydash.get(item, "_id.status")
        count = pydash.get(item, "count")

        # Update status_summary dictionary
        if competitor not in status_summary:
            status_summary[competitor] = {"status_200_count": 0, "other_status_count": 0}

        if status == 200:
            status_summary[competitor]["status_200_count"] += count
        else:
            status_summary[competitor]["other_status_count"] += count

    csv_filename = "summary_status_count.csv"
    with open(csv_filename, mode="w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Competitor", "status_200_count", "other_status_count"])
        for competitor, counts in status_summary.items():
            csv_writer.writerow([competitor, counts["status_200_count"], counts["other_status_count"]])
    return csv_filename


def competitors_with_no_offers_summary():
    no_offer_summary = {}
    days_ago = timedelta(days=7)
    start_date = datetime.now() - days_ago
    pipeline = [
        {
            "$match": {"captured_at": {"$gte": start_date}, "$or": [{"offers": {"$exists": False}}, {"offers": {"$size": 0}}]},
        },
        {"$group": {"_id": "$competitor", "count": {"$sum": 1}, "urls": {"$push": "$url"}}},
        {"$limit": 10},
        {"$project": {"_id": 1, "count": 1, "urls": 1}},
    ]
    results = db.competitorproducts.aggregate(pipeline)
    for item in results:
        competitor = item["_id"]
        count = item["count"]
        urls = item["urls"]
        no_offer_summary[competitor] = {"count": count, "urls": urls}

    csv_filename = "no_offers_count.csv"
    with open(csv_filename, mode="w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Competitor", "no_offer_count", "urls"])
        for competitor, obj in no_offer_summary.items():
            csv_writer.writerow([competitor, obj["count"], obj["urls"]])
    return csv_filename


def scraped_data_summary():
    try:
        periods = [7, 45, 90]
        competitor_data = {}

        # Collect data for each period
        for period in periods:
            days_ago = timedelta(days=period)
            start_date = datetime.now() - days_ago

            pipeline = [{"$match": {"captured_at": {"$gte": start_date}}}, {"$group": {"_id": "$competitor", "count": {"$sum": 1}}}]

            results = db.competitorproducts.aggregate(pipeline)

            # Store data for each competitor for this period
            for result in results:
                competitor = result["_id"]
                count = result["count"]
                if competitor not in competitor_data:
                    competitor_data[competitor] = {7: 0, 45: 0, 90: 0}  # Initialize counts for each period
                competitor_data[competitor][period] = count

        # Write data to CSV file
        csv_filename = "summary_all_periods.csv"
        with open(csv_filename, mode="w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["Competitor", "Count (last 7 days)", "Count (last 45 days)", "Count (last 90 days)"])
            for competitor, counts in competitor_data.items():
                csv_writer.writerow([competitor, counts[7], counts[45], counts[90]])

        status_summary_file = urls_code_data()
        no_offer_sumary = competitors_with_no_offers_summary()
        files = [csv_filename, status_summary_file, no_offer_sumary]
        uploaded_files = []
        for i in files:
            link = upload_to_google_drive(i, max_trys=10, init=0)
            if link:
                uploaded_files.append(link)
        email_with_attachments(SUBJECT, RECEIVER, JOB, uploaded_files, CC)
    except Exception as e:
        send_detailed_slack_message("competitor-url-files-error", str(e))
