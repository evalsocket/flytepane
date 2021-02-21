
from flytekit import task, workflow, LaunchPlan, current_context
import pandas
import pandas as pd
import altair as alt
import datapane as dp
from flytekit.types import schema  # noqa: F401
#from replit import db

# Endpoint: 127.0.0.1:30081
# Dashboard: 127.0.0.1:30081/console
# Report: datapane.com/evalsocket
@task
def publish_report(df: pandas.DataFrame):
    dp_token: str = db["DP_TOKEN"]
    dp.login(token=dp_token)

    plot = alt.Chart(df).mark_area(opacity=0.4, stroke='black').encode(
        x='date:T',
        y=alt.Y('new_cases_smoothed_per_million:Q', stack=None),
        color=alt.Color('continent:N', scale=alt.Scale(scheme='set1')),
        tooltip='continent:N').interactive().properties(width='container')

    dp.Report(dp.Plot(plot), dp.DataTable(df)).save(path='report.html',open=True)


@task
def transform_data(url: str) -> pandas.DataFrame:
    dataset = pd.read_csv(url)
    df = dataset.groupby(
        ['continent',
         'date'])['new_cases_smoothed_per_million'].mean().reset_index()
    return df


@workflow
def datapane_workflow(url: str):
    df = transform_data(url=url)
    publish_report(df=df)
    print(f"Report is published for {url}")


default_lp = LaunchPlan.get_default_launch_plan(
    current_context(),
    datapane_workflow)

if __name__ == "__main__":
    print(default_lp(url="https://covid.ourworldindata.org/data/owid-covid-data.csv"))

