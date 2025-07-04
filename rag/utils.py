import pandas as pd


def load_dataset(ds_link: str) -> pd.DataFrame:
    """
    This function loads dataset and saves it to the local database.

    Args:
        ds_link: str
            Link of the dataset that should be loaded.
    Returns:
        pd.Dataframe
    """

    return pd.read_csv(ds_link)


# "hf://datasets/lvimuth/HealthRisk-1500-Medical-Risk-Prediction/Full_Patient_Risk_Prediction_Dataset.csv"
