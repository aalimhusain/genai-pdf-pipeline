from extractor import extract_all
from database import init_db, save_results, export_to_csv

def run_pipeline():
    # Initialize DB
    init_db()

    # Example texts
    texts = [
        "On 15/10/2025 Aalim met Husain at the Xorstack in Bengaluru."
    ]

    # Extract entities
    results = []
    for text in texts:
        res = extract_all(text)
        res["text"] = text
        results.append(res)

    # Save to DB
    request_id = save_results(results)
    print(f"💾 Saved batch to database. Request ID: {request_id}")

    # Export only this batch to CSV
    csv_file = export_to_csv(request_id)
    print(f"📤 Exported current batch to {csv_file}")

if __name__ == "__main__":
    run_pipeline()
