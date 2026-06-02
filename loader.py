import pandas as pd


class DatasetLoader:

    @staticmethod
    def detect_header(df_preview):

        best_row = 0
        best_score = -1

        for idx in range(len(df_preview)):

            row = df_preview.iloc[idx]

            score = row.notna().sum()

            if score > best_score:

                best_score = score
                best_row = idx

        return best_row

    @staticmethod
    def load_file(uploaded_file):

        file_name = uploaded_file.name.lower()

        try:

            if file_name.endswith(".csv"):

                preview = pd.read_csv(
                    uploaded_file,
                    header=None,
                    nrows=20,
                    encoding_errors="ignore"
                )

                header_row = DatasetLoader.detect_header(
                    preview
                )

                uploaded_file.seek(0)

                df = pd.read_csv(
                    uploaded_file,
                    header=header_row,
                    encoding_errors="ignore"
                )

            elif file_name.endswith(
                (".xlsx", ".xls")
            ):

                preview = pd.read_excel(
                    uploaded_file,
                    header=None,
                    nrows=20
                )

                header_row = DatasetLoader.detect_header(
                    preview
                )

                uploaded_file.seek(0)

                df = pd.read_excel(
                    uploaded_file,
                    header=header_row
                )

            else:

                raise ValueError(
                    "Unsupported file format"
                )

        except Exception as e:

            raise Exception(
                f"Unable to load dataset: {e}"
            )

        df.columns = (

            df.columns
            .astype(str)
            .str.strip()
            .str.replace("\n", " ")
        )

        return df
