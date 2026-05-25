import pandas as pd
class DatasetLoader:
    @staticmethod
    def load_file(uploaded_file):
        try:
            # CSV File
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)

            # Excel File
            elif uploaded_file.name.endswith(".xlsx"):
                df = pd.read_excel(uploaded_file)

            else:
                raise ValueError("Unsupported file format")
            # Remove fully empty rows
            df = df.dropna(how='all')
            return df
        except Exception as e:

            raise Exception(
                f"Error loading dataset: {e}"
            )
