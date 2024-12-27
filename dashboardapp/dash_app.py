from shiny import App, Inputs, Outputs, Session, render, ui
import shinyswatch
from dashboardapp.plots import plotui, plotui2, server1, server2

# ui 
app_ui = ui.page_fillable(
    ui.layout_columns(plotui("plot1"),
                plotui2("plot2")),
               theme=shinyswatch.theme.sandstone)

# server
def server(input: Inputs, output: Outputs, session: Session):
    server1("plot1")
    server2("plot2")
    
# app
app = App(app_ui, server)
