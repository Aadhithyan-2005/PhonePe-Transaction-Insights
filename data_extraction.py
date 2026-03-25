import os
import json
import pandas as pd

PULSE_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pulse", "data")

def iter_json_files(base_path):
    """Walk state/year/quarter JSON files and yield parsed data."""
    india_path = os.path.join(base_path, "country", "india", "state")
    if not os.path.exists(india_path):
        print(f"[WARNING] Path not found: {india_path}")
        return
    for state in sorted(os.listdir(india_path)):
        state_path = os.path.join(india_path, state)
        if not os.path.isdir(state_path):
            continue
        for year in sorted(os.listdir(state_path)):
            year_path = os.path.join(state_path, year)
            if not os.path.isdir(year_path):
                continue
            for fname in sorted(os.listdir(year_path)):
                if not fname.endswith(".json"):
                    continue
                quarter = int(fname.replace(".json", ""))
                with open(os.path.join(year_path, fname), "r") as f:
                    data = json.load(f)
                yield state, int(year), quarter, data

def extract_aggregated_transaction():
    records = []
    for state, year, quarter, data in iter_json_files(
            os.path.join(PULSE_ROOT, "aggregated", "transaction")):
        for tx in data.get("data", {}).get("transactionData", []):
            for pi in tx.get("paymentInstruments", []):
                records.append({"state": state, "year": year, "quarter": quarter,
                    "transaction_type": tx.get("name"),
                    "transaction_count": pi.get("count", 0),
                    "transaction_amount": pi.get("amount", 0.0)})
    df = pd.DataFrame(records)
    print(f"[aggregated_transaction] {len(df)} rows")
    return df

def extract_aggregated_user():
    records = []
    for state, year, quarter, data in iter_json_files(
            os.path.join(PULSE_ROOT, "aggregated", "user")):
        agg = data.get("data", {}).get("aggregated", {})
        devices = data.get("data", {}).get("usersByDevice") or []
        if devices:
            for dev in devices:
                records.append({"state": state, "year": year, "quarter": quarter,
                    "registered_users": agg.get("registeredUsers", 0),
                    "app_opens": agg.get("appOpens", 0),
                    "brand": dev.get("brand"),
                    "device_count": dev.get("count", 0),
                    "device_percentage": dev.get("percentage", 0.0)})
        else:
            records.append({"state": state, "year": year, "quarter": quarter,
                "registered_users": agg.get("registeredUsers", 0),
                "app_opens": agg.get("appOpens", 0),
                "brand": None, "device_count": 0, "device_percentage": 0.0})
    df = pd.DataFrame(records)
    print(f"[aggregated_user] {len(df)} rows")
    return df

def extract_aggregated_insurance():
    records = []
    for state, year, quarter, data in iter_json_files(
            os.path.join(PULSE_ROOT, "aggregated", "insurance")):
        for tx in data.get("data", {}).get("transactionData", []):
            for pi in tx.get("paymentInstruments", []):
                records.append({"state": state, "year": year, "quarter": quarter,
                    "insurance_type": tx.get("name"),
                    "transaction_count": pi.get("count", 0),
                    "transaction_amount": pi.get("amount", 0.0)})
    df = pd.DataFrame(records)
    print(f"[aggregated_insurance] {len(df)} rows")
    return df

def extract_map_transaction():
    records = []
    for state, year, quarter, data in iter_json_files(
            os.path.join(PULSE_ROOT, "map", "transaction", "hover")):
        for item in data.get("data", {}).get("hoverDataList", []):
            for metric in item.get("metric", []):
                records.append({"state": state, "year": year, "quarter": quarter,
                    "district": item.get("name"),
                    "transaction_count": metric.get("count", 0),
                    "transaction_amount": metric.get("amount", 0.0)})
    df = pd.DataFrame(records)
    print(f"[map_transaction] {len(df)} rows")
    return df

def extract_map_user():
    records = []
    for state, year, quarter, data in iter_json_files(
            os.path.join(PULSE_ROOT, "map", "user", "hover")):
        for district, vals in data.get("data", {}).get("hoverData", {}).items():
            records.append({"state": state, "year": year, "quarter": quarter,
                "district": district,
                "registered_users": vals.get("registeredUsers", 0),
                "app_opens": vals.get("appOpens", 0)})
    df = pd.DataFrame(records)
    print(f"[map_user] {len(df)} rows")
    return df

def extract_map_insurance():
    records = []
    for state, year, quarter, data in iter_json_files(
            os.path.join(PULSE_ROOT, "map", "insurance", "hover")):
        for item in data.get("data", {}).get("hoverDataList", []):
            for metric in item.get("metric", []):
                records.append({"state": state, "year": year, "quarter": quarter,
                    "district": item.get("name"),
                    "transaction_count": metric.get("count", 0),
                    "transaction_amount": metric.get("amount", 0.0)})
    df = pd.DataFrame(records)
    print(f"[map_insurance] {len(df)} rows")
    return df

def extract_top_transaction():
    records = []
    for state, year, quarter, data in iter_json_files(
            os.path.join(PULSE_ROOT, "top", "transaction")):
        for level in ["districts", "pincodes"]:
            for item in data.get("data", {}).get(level, []):
                metric = item.get("metric", {})
                records.append({"state": state, "year": year, "quarter": quarter,
                    "entity_type": level.rstrip("s"),
                    "entity_name": item.get("entityName"),
                    "transaction_count": metric.get("count", 0),
                    "transaction_amount": metric.get("amount", 0.0)})
    df = pd.DataFrame(records)
    print(f"[top_transaction] {len(df)} rows")
    return df

def extract_top_user():
    records = []
    for state, year, quarter, data in iter_json_files(
            os.path.join(PULSE_ROOT, "top", "user")):
        for level in ["districts", "pincodes"]:
            for item in data.get("data", {}).get(level, []):
                records.append({"state": state, "year": year, "quarter": quarter,
                    "entity_type": level.rstrip("s"),
                    "entity_name": item.get("name"),
                    "registered_users": item.get("registeredUsers", 0)})
    df = pd.DataFrame(records)
    print(f"[top_user] {len(df)} rows")
    return df

def extract_top_insurance():
    records = []
    for state, year, quarter, data in iter_json_files(
            os.path.join(PULSE_ROOT, "top", "insurance")):
        for level in ["districts", "pincodes"]:
            for item in data.get("data", {}).get(level, []):
                metric = item.get("metric", {})
                records.append({"state": state, "year": year, "quarter": quarter,
                    "entity_type": level.rstrip("s"),
                    "entity_name": item.get("entityName"),
                    "transaction_count": metric.get("count", 0),
                    "transaction_amount": metric.get("amount", 0.0)})
    df = pd.DataFrame(records)
    print(f"[top_insurance] {len(df)} rows")
    return df

def extract_all():
    print("="*50)
    print("Extracting all PhonePe Pulse data...")
    print("="*50)
    return {
        "aggregated_transaction": extract_aggregated_transaction(),
        "aggregated_user":        extract_aggregated_user(),
        "aggregated_insurance":   extract_aggregated_insurance(),
        "map_transaction":        extract_map_transaction(),
        "map_user":               extract_map_user(),
        "map_insurance":          extract_map_insurance(),
        "top_transaction":        extract_top_transaction(),
        "top_user":               extract_top_user(),
        "top_insurance":          extract_top_insurance(),
    }

if __name__ == "__main__":
    dfs = extract_all()
    print("\nSample - aggregated_transaction:")
    print(dfs["aggregated_transaction"].head())