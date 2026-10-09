# Adaptive Predictive Maintenance

In this folder are the first steps of my research. A simple basline model trained with randomforest.
Also there are waveform plots for engines.

## Where to find things

The baseline model: in CMAPSS/Model.py
The engine plots: CMAPSS/test.py
Plots for the basemodel: CMAPSS/plot.py

Results are saved in: CMAPSS/figures

## Preparing the enviroment

You should run the project in a python enviroment, with the 3.11 python version (Otherwise the pdmdata library doesnt work)

In requirements.txt you can find the project imported libraries

## What I did

I trained a baseline model on subset FD001. The 100 train engines are split per engine: 80 engines to train the model and 20 engines as a stream. The stream engines are given to the model one by one, cycle by cycle, without any drift.

Based on what's useful to know I made these plots first:

- **Error stream:** shows the absolute error per cycle in the order the engines come in. This is the signal a drift detector will work on, so I need to know what it looks like without drift.
- **Predicted vs actual:** shows how far the predicted RUL is from the actual RUL, and if the model predicts too high or too low.
- **Error vs actual RUL:** shows if the error depends on the life phase of an engine (healthy at the start, wear until failure).
- **One engine:** shows how the model behaves for one engine from the first cycle until failure.

## What I found

- **Error stream:** the error is not stable and has big peaks per engine, even without drift. A drift detector could give false alarms on this.
- **Predicted vs actual:** close to failure the predictions are good. Between an RUL of about 25 and 150 the model mostly predicts too high. Above an RUL of about 200 the prediction stays around 150.
- **Error vs actual RUL:** the error is big at the start of an engine's life, rises again around an RUL of 50–100 and is small close to failure. So a rising error does not always mean drift.
- **One engine:** the prediction jumps a lot from cycle to cycle, but gets accurate in the last cycles before failure.

Baseline result (seed 0): MAE 32.5 cycles, RMSE 44.1 cycles.

## My questions

As said the errorstream is not stable, is this problem for later on. Is there a way to mimize this or something. How do I deal with this?

Did I train correctly, are these valid takes from the plot?