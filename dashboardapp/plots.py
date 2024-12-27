from shiny import Inputs, Outputs, Session, render, ui, module
import shinyswatch
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import StringIO

@module.ui
def plotui(): #degrees by dept ui
    return ui.card(ui.card_header("BA Degrees by Department"),
                   ui.input_select("Major","Major:",{"Division of the Arts":
                                    {11:"Art",12:"Dance",13:"Music",14:"Theatre"}, 
                                    "Division of History and Social Sciences":
                                    {21:"Anthropology",22:"Economics",23:"History",
                                     24:"Political Science", 25:"Sociology"},
                                    "Division of Literature and Languages":
                                    {31:"Ancient Mediterranean Studies",32:"Chinese",
                                    33:"Classics",34:"Comparative Lit.",35:"English",
                                    36:"French",37:"German",38:"Russian",39:"Spanish"},
                                    "Division of Mathematics and Natural Sciences":
                                    {41: "Biology", 42: "Chemistry", 43: "Computer Science",
                                    44: "Mathematics",45: "Physics" },
                                    "Division of Philosophy, Religion, Psychology and Linguistics":
                                    {51:"Linguistics",52:"Philosophy", 53:"Psychology",54:"Religion"}}),
                                    ui.output_plot("plot1"))
     
@module.ui #retention rates ui
def plotui2(): 
    return ui.card(ui.card_header("Retention Rate vs Time"),
                   ui.input_selectize("Year","Select Years:",{1: "2nd Year",2:"3rd Year", 3:"4th Year"},multiple=True),
                   ui.output_plot("plot2"))

@module.server
def server1(input: Inputs, output: Outputs, session: Session):
    @output
    @render.plot
    def plot1(): #degrees by dept plot
        r = requests.get("https://www.reed.edu/ir/gradbydept.html")
        soup = BeautifulSoup(r.content, 'html.parser')
        division = int(input.Major()[0]) -1
        major = int(input.Major()[1])
        table = soup.find_all("table")[division]
        df = pd.read_html(StringIO(str(table)))[0]
        df.columns = [' '.join(col).strip() for col in df.columns]
        df = df.set_index('Unnamed: 0_level_0 Unnamed: 0_level_1').transpose()
        for i in range(0,len(df.columns)):
            df.iloc[0:,i]=pd.to_numeric(df.iloc[0:,i],errors='coerce').fillna(0)
        women = []
        men = []
        total = []
        for i in range(0,len(df.index)):
            if "Wmn" in df.index[i]:
                women.append(df.iloc[i,:])
            elif "Men" in df.index[i]:
                men.append(df.iloc[i,:])
            else:
                total.append(df.iloc[i,:])
        women = pd.DataFrame(women).reset_index()
        men = pd.DataFrame(men).reset_index()
        total = pd.DataFrame(total).reset_index()
        fig, ax = plt.subplots()
        ax.plot(women.index,women.iloc[:,major],"o-",label="Women")
        ax.plot(men.index,men.iloc[:,major],"o-",label="Men")
        ax.plot(total.index,total.iloc[:,major],"o--c",label="Total")
        ax.set_xticks(women.index,['2020','2021','2022','2023','2024'])
        ax.set_title("Degrees Granted")
        ax.legend()
        print(df)
        ax.set_xlabel("Year")
        ax.set_ylabel("Count")
        ax.set_ylim(0,max(total.iloc[:,major])+7)
        return fig


@module.server
def server2(input: Inputs, output: Outputs, session: Session):
    @output
    @render.plot
    def plot2(): #retention rates plot
        r1 = requests.get("https://www.reed.edu/ir/retentionrates.html")
        soup1 = BeautifulSoup(r1.content, 'html.parser')
        s1 = soup1.find('table', class_="table")
        content = s1.find_all('td')
        table = soup1.find_all('table')[0]
        rows = table.find_all('tr')
        data1 = pd.DataFrame([])
        for i in rows[2:]:
            index = i.find('th')
            year = index.text.strip()
            year = int(year)
            cells = i.find_all('td')
            count = cells[0].text.strip()
            secondyr = pd.to_numeric(cells[1].text.strip().strip('%'),errors='coerce')
            thirdyr = pd.to_numeric(cells[2].text.strip().strip('%'),errors='coerce')
            fourthyr = pd.to_numeric(cells[3].text.strip().strip('%'),errors='coerce')
            row_list = pd.DataFrame([[year,count,secondyr,thirdyr,fourthyr]])
            data1 = pd.concat([data1,row_list])
        data1 = pd.DataFrame(data1).reset_index()
        fig, ax = plt.subplots()
        for i in input.Year():
            ax.plot(data1[0],data1[int(i)+1],label=f"{int(i)+1}")
        ax.set_ylim(0,100)
        ax.set_xlim(1980,2024)
        ax.set_xlabel("Class (Year of Entry)")
        ax.set_ylabel("Retention Rate")
        ax.legend()
        print(input.Year())
        return fig