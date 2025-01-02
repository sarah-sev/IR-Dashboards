from shiny import App, Inputs, Outputs, Session, render, ui
import shinyswatch
from dashboardapp.plots import plotui, plotui2, plotui3, plotui4, server1, server2, server3,server4

# ui 
app_ui = ui.page_fluid(
    ui.navset_tab(
        ui.nav_panel("Degrees Granted",ui.layout_columns(plotui("plot1"),
                                                         col_widths={"sm": (-2, 7, 2)})),
        ui.nav_panel("Retention Rates",ui.layout_columns(plotui2("plot2"),
                                                         col_widths={"sm": (-2, 7, 2)})),
        ui.nav_panel("Admissions",ui.layout_columns(plotui3("plot3"),plotui4("plot4"))),
    ),
        theme=shinyswatch.theme.sandstone)

# server
def server(input: Inputs, output: Outputs, session: Session):
    server1("plot1")
    server2("plot2")
    server3("plot3")
    server4("plot4")
    
# app
app = App(app_ui, server)
