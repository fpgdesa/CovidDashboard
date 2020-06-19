from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth.backends import RemoteUserBackend

from plotly.offline import plot
from plotly.graph_objs import Scatter
import pandas as pd
import plotly.offline as py
import cufflinks as cf
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import os
from django.conf import settings
from django.contrib.staticfiles import finders
from datetime import datetime,timedelta


class DashboardFront(View):
    def get(self,request):
        return render(request,"dashboard/index.html")



class DashboardPaty(View):

    def transform_week(self,x):

        d = '2020-W'+str(x)
        start = datetime.strptime(d + '-1', '%G-W%V-%u')

        end = start + timedelta(6)

        start = start.strftime("%d/%m/%Y")

        end =  end.strftime("%d/%m/%Y")

        return start + " - " + end

    
    def get(self,request):
    
        data_path = finders.find('Dados_paty.csv')

        data = pd.read_csv(data_path)


#        trace = plot([Scatter(x = data['Data'],
 #                  y = data['Confirmados'],
  #                 mode = 'lines')],output_type='div')
        
       
        data2 = data.set_index('Data')

        fig = data2[['Confirmados']].iplot(asFigure=True, kind='scatter',
               xTitle='Data',
               yTitle='Número de Casos',
               vspan={'x0':'08/06/20','x1':data2.iloc[-1].name,
               'color':'rgba(0,0,50,0.3)','fill':True,'opacity':.3})

        fig.update_layout(
               showlegend=False,
               annotations=[
               dict(
               x=data2.iloc[-1].name,
               y=data2['Confirmados'].iloc[-1],
               xref="x",
               yref="y",
               text="<b>" + str(data2['Confirmados'].iloc[-1]) + " casos em " + str(data2.iloc[-1].name) + "<b>",
               showarrow=True,
               arrowhead=7,
               ax=0,
               ay=-40)])

        fig['data'][0]['line'] = {
            'color': 'rgba(63, 63, 190, 1.0)', 'dash': 'solid', 'shape': 'linear', 'width': 3.0}

        trace =  plot(fig, include_plotlyjs=True, output_type='div')


        bar_fig = go.Bar(x = data['Data'],
                   y = data['Novos Suspeitos'],
                   offsetgroup=0)

        layout = go.Layout(
                 paper_bgcolor='rgba(0,0,0,0)',
                 plot_bgcolor='rgba(0,0,0,0)')

        dat = [bar_fig]

        figura_bar= go.Figure(data=dat, layout=layout)
        
        trace2 = plot(figura_bar, include_plotlyjs=True, output_type='div')

        confirmados = str(data2['Confirmados'].iloc[-1])

        curados = str(int(data2['Curados'].iloc[-1]))

        internados = str(int(data2['Internados'].iloc[-1]))


        obitos = str(int(data2['Obitos'].iloc[-1]))

        ultima_atu = data2.iloc[-1].name


        # Grafico Soma de casos semanais



        [datetime.strptime(x, '%d/%m/%y') for x in data['Data'].values][-1].strftime("%V")

        soma_confirmados_semanal = pd.DataFrame(columns=['Semana', 'Casos'])

        convert = lambda date: datetime.strptime(date, '%d/%m/%y')

        for i in range(len(data) ):

            data_atual = convert(data['Data'].values[i])

            semana = data_atual.strftime("%V")

            conta_casos = data['Confirmados'][i]

            soma_confirmados_semanal.loc[i] = [semana] + [conta_casos]


        soma_confirmados_semanal['Novos Casos'] = soma_confirmados_semanal['Casos'].diff().fillna(soma_confirmados_semanal['Casos'].iloc[0])


        soma_confirmados_semanal_consolidado  = soma_confirmados_semanal[['Semana','Novos Casos']].groupby('Semana').sum()


        soma_confirmados_semanal_consolidado['Semana_str'] = [self.transform_week(int(x)) for x in soma_confirmados_semanal_consolidado.index]


        bar_soma_casos_semanais = go.Bar(x = soma_confirmados_semanal_consolidado['Semana_str'],
               y = soma_confirmados_semanal_consolidado['Novos Casos'],
               offsetgroup=0)

        layout_bar_soma_casos_semanais = go.Layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
                )

        dat_soma_casos_sem = [bar_soma_casos_semanais]

        figura_bar_casos_semanais = go.Figure(data=dat_soma_casos_sem,layout=layout_bar_soma_casos_semanais)

        trace_casos_semanais = plot(figura_bar_casos_semanais, include_plotlyjs=True, output_type='div')

        
        return render(request,"dashboard/cidades/paty/paty.html", context={'plot_div': trace,'bar_suspeitos': trace2, 'confirmados':confirmados,'curados':curados,'internados':internados,'obitos':obitos,'ultima_atu': ultima_atu,'plot_bar_sem':trace_casos_semanais})



class DashboardMiguel(View):

    def transform_week(self,x):

        d = '2020-W'+str(x)
        start = datetime.strptime(d + '-1', '%G-W%V-%u')

        end = start + timedelta(6)

        start = start.strftime("%d/%m/%Y")

        end =  end.strftime("%d/%m/%Y")

        return start + " - " + end

    
    def get(self,request):
    
        data_path = finders.find('Dados_miguel.csv')

        data = pd.read_csv(data_path)


#        trace = plot([Scatter(x = data['Data'],
 #                  y = data['Confirmados'],
  #                 mode = 'lines')],output_type='div')
        
       
        data2 = data.set_index('Data')

        fig = data2[['Confirmados']].iplot(asFigure=True, kind='scatter',
               xTitle='Data',
               yTitle='Número de Casos',
               vspan={'x0':'01/06/20','x1':data2.iloc[-1].name,
               'color':'rgba(0,0,50,0.3)','fill':True,'opacity':.3})

        fig.update_layout(
               showlegend=False,
               annotations=[
               dict(
               x=data2.iloc[-1].name,
               y=data2['Confirmados'].iloc[-1],
               xref="x",
               yref="y",
               text="<b>" + str(data2['Confirmados'].iloc[-1]) + " casos em " + str(data2.iloc[-1].name) + "<b>",
               showarrow=True,
               arrowhead=7,
               ax=0,
               ay=-40)])

        fig['data'][0]['line'] = {
            'color': 'rgba(63, 63, 190, 1.0)', 'dash': 'solid', 'shape': 'linear', 'width': 3.0}

        trace =  plot(fig, include_plotlyjs=True, output_type='div')


        bar_fig = go.Bar(x = data['Data'],
                   y = data['Novos Suspeitos'],
                   offsetgroup=0)

        layout = go.Layout(
                 paper_bgcolor='rgba(0,0,0,0)',
                 plot_bgcolor='rgba(0,0,0,0)')

        dat = [bar_fig]

        figura_bar= go.Figure(data=dat,layout=layout)
        
        trace2 = plot(figura_bar, include_plotlyjs=True, output_type='div')

        confirmados = str(data2['Confirmados'].iloc[-1])

        curados = str(int(data2['Curados'].iloc[-1]))

        internados = str(int(data2['Internados'].iloc[-1]))


        obitos = str(int(data2['Obitos'].iloc[-1]))

        ultima_atu = data2.iloc[-1].name


        # Grafico Soma de casos semanais



        [datetime.strptime(x, '%d/%m/%y') for x in data['Data'].values][-1].strftime("%V")

        soma_confirmados_semanal = pd.DataFrame(columns=['Semana', 'Casos'])

        convert = lambda date: datetime.strptime(date, '%d/%m/%y')

        for i in range(len(data) ):

            data_atual = convert(data['Data'].values[i])

            semana = data_atual.strftime("%V")

            conta_casos = data['Confirmados'][i]

            soma_confirmados_semanal.loc[i] = [semana] + [conta_casos]


        soma_confirmados_semanal['Novos Casos'] = soma_confirmados_semanal['Casos'].diff().fillna(soma_confirmados_semanal['Casos'].iloc[0])


        soma_confirmados_semanal_consolidado  = soma_confirmados_semanal[['Semana','Novos Casos']].groupby('Semana').sum()


        soma_confirmados_semanal_consolidado['Semana_str'] = [self.transform_week(int(x)) for x in soma_confirmados_semanal_consolidado.index]


        bar_soma_casos_semanais = go.Bar(x = soma_confirmados_semanal_consolidado['Semana_str'],
               y = soma_confirmados_semanal_consolidado['Novos Casos'],
               offsetgroup=0)


        layout_bar_soma_casos_semanais = go.Layout(
                 paper_bgcolor='rgba(0,0,0,0)',
                 plot_bgcolor='rgba(0,0,0,0)')


        dat_soma_casos_sem = [bar_soma_casos_semanais]

        figura_bar_casos_semanais = go.Figure(data=dat_soma_casos_sem,layout=layout_bar_soma_casos_semanais)

        trace_casos_semanais = plot(figura_bar_casos_semanais, include_plotlyjs=True, output_type='div')
        
        return render(request,"dashboard/cidades/miguel/miguel.html", context={'plot_div_miguel': trace,'bar_suspeitos_miguel': trace2, 'confirmados_miguel':confirmados,'curados_miguel':curados,'internados_miguel':internados,'obitos_miguel':obitos,'ultima_atu_miguel': ultima_atu,'plot_bar_sem_miguel':trace_casos_semanais})



