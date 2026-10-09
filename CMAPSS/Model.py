
import pdmdata
from pdmdata.datasets.cmapss import inventory
from pdmdata.tasks.rul import prepare_cmapss
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from plot import plot_results

"""
This file contains a model trained by randomforest. It will output a series of graphs
"""

_subset = "FD001"

def main():
    pdmdata.download("cmapss")  # hergebruikt een bestaande download
    summary = inventory()
    print(summary)
    print(f"Train/test trajectories: {summary['units'].sum():,}; cycle rows: {summary['rows'].sum():,}")

    #Split set
    X_train, Y_train, X_stream, Y_stream, stream = split_set(_subset)
    prediction, abs_error = train_randomforest(xt=X_train, yt=Y_train, xs=X_stream, ys=Y_stream)
    plot_results(stream, Y_stream, prediction, abs_error)


def split_set(_subset):
    bundle = prepare_cmapss(
        _subset,
        rul_cap=None,
        validation_fraction=0.2,
        random_state=0,
        drop_constant_features=True,
    )

    train = bundle.train.frame
    stream = bundle.validation.frame

    features = list(bundle.feature_columns)
    X_train = train.select(features).to_numpy()
    Y_train = train["RUL"].to_numpy()

    stream = stream.sort(["unit_number", "cycle"])
    X_stream = stream.select(features).to_numpy()
    Y_stream = stream["RUL"].to_numpy()

    return X_train, Y_train, X_stream, Y_stream, stream


def train_randomforest(xt, yt, xs, ys):
    model = RandomForestRegressor(
        n_estimators=100,
        min_samples_leaf=5,
        random_state=0,
        n_jobs=-1,
    )
    model.fit(xt, yt)

    prediction = model.predict(xs)
    abs_error = np.abs(prediction - ys)

    print("MAE :", abs_error.mean())
    print("RMSE:", np.sqrt(np.mean((prediction - ys) ** 2)))

    return prediction, abs_error


if __name__ == "__main__":
    main()
