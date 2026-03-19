from fastapi import UploadFile
import pandas as pd
import io

class ZerodhaFileService:

    async def parse_file(self, file: UploadFile) -> dict:
            file_bytes = await file.read()
            # Load raw sheet without headers
            raw_df = pd.read_excel(io.BytesIO(file_bytes), header=None)

            # Find the row where the table header starts
            header_row = None
            for idx, row in raw_df.iterrows():
                if "Symbol" in row.values:
                    header_row = idx
                    break

            if header_row is None:
                raise ValueError("Could not locate stock table in Zerodha export")

            # Extract header
            headers = raw_df.iloc[header_row].tolist()

            # Extract table rows
            table_df = raw_df.iloc[header_row + 1:].copy()
            table_df.columns = headers

            # Remove empty rows
            table_df = table_df[table_df["Symbol"].notna()]

            # Select relevant columns
            table_df = table_df[
                [
                    "Symbol",
                    "Open Quantity",
                    "Open Value",
                    "Unrealized P&L",
                    "Unrealized P&L Pct."
                ]
            ]

            # Rename columns
            table_df = table_df.rename(
                columns={
                    "Symbol": "stock",
                    "Open Quantity": "quantity",
                    "Open Value": "investment",
                    "Unrealized P&L": "total_gain_loss",
                    "Unrealized P&L Pct.": "performance_pct"
                }
            )
            table_df = table_df.fillna(0)    
            return table_df.to_dict(orient="records")