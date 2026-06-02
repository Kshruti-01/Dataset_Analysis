import pandas as pd


class DatasetProfiler:

    def __init__(self, df):

        self.df = df

    def generate_profile(self):

        profile = {}

        profile["rows"] = len(self.df)

        profile["columns"] = len(self.df.columns)

        profile["duplicates"] = (
            self.df.duplicated().sum()
        )

        profile["missing_values"] = (
            self.df.isna()
            .sum()
            .sum()
        )

        profile["memory_usage_mb"] = round(
            self.df.memory_usage(
                deep=True
            ).sum() / (1024 * 1024),
            2
        )

        profile["column_types"] = (
            self.df.dtypes
            .astype(str)
            .to_dict()
        )

        return profile

    def quality_score(self):

        score = 100

        missing_pct = (
            self.df.isna()
            .sum()
            .sum()
            /
            (self.df.shape[0]
             * self.df.shape[1])
        ) * 100

        duplicate_pct = (
            self.df.duplicated()
            .sum()
            /
            max(len(self.df), 1)
        ) * 100

        score -= min(
            missing_pct * 0.5,
            30
        )

        score -= min(
            duplicate_pct * 0.5,
            20
        )

        return round(
            max(score, 0),
            2
        )
