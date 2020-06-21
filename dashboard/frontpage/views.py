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
import numpy as np



class DashboardFront(View):
    def get(self,request):
        return render(request,"dashboard/index.html")


class DashboardPaty(View):

    def loadFile(self, file):
        
        data_path = finders.find(file)

        return pd.read_csv(data_path)

    def getPopulationPyramidGraph(self):

        dados_contaminados_paty = self.loadFile('Contaminados_paty.csv')

        dados_obitos_paty = self.loadFile('Obitos_paty.csv')

        mulheres_contaminadas_paty = dados_contaminados_paty[dados_contaminados_paty['Sexo'] == "Feminino"][['Idade']]

        homens_contaminados_paty = dados_contaminados_paty[dados_contaminados_paty['Sexo']=='Masculino'][['Idade']]

        mulheres_obito_paty = dados_obitos_paty[dados_obitos_paty['Sexo']=='Feminino'][['Idade']]

        homens_obito_paty = dados_obitos_paty[dados_obitos_paty['Sexo']=='Masculino'][['Idade']]

        intervalo_idade = np.arange(0,110,10)

        mulheres_contaminadas_paty_cons = mulheres_contaminadas_paty.groupby(pd.cut(mulheres_contaminadas_paty.Idade, intervalo_idade)).count()

        homens_contaminadas_paty_cons = homens_contaminados_paty.groupby(pd.cut(homens_contaminados_paty.Idade, intervalo_idade)).count()

        mulheres_obito_paty_cons = mulheres_obito_paty.groupby(pd.cut(mulheres_obito_paty.Idade, intervalo_idade)).count()

        homens_obito_paty_cons = homens_obito_paty.groupby(pd.cut(homens_obito_paty.Idade, intervalo_idade)).count()


        a = 0.55
        b = 9.5
        c = -0.5

        yidx =np.arange(10)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=-1*mulheres_contaminadas_paty_cons.to_numpy().flatten(),
                            y=yidx,
                            orientation='h',
                            name='Mulheres',
                            width=1,
                            customdata=-1*mulheres_contaminadas_paty_cons.to_numpy().flatten(),
                            hovertemplate = "%{customdata}",
                            marker=dict(color='cornflowerblue')
                            ))

        fig.add_trace(go.Bar(x= homens_contaminadas_paty_cons.to_numpy().flatten(),
                            y= yidx,
                            orientation='h',
                            width=1,
                            name= 'Homens',
                            hovertemplate="%{x}",
                            marker=dict(color='lightblue')))  
        fig.add_scatter(x=[-a, a, a, -a],
                        y= [b, b, c, c], fill='toself',
                        mode='lines',
                        fillcolor='white' , line_color='white',
                        showlegend=False,
                        )
        fig.add_scatter(x= [0 ]*10,
                        y=yidx,
                        text=["0-10 ","10-20","20-30","30-40","40-50","50-60","60-70","70-80","80-90","90-100"],
                        mode='text',
                        showlegend=False,
                        )

        fig.add_trace( go.Bar(y=yidx,
                    x=homens_obito_paty_cons.to_numpy().flatten(),
                    orientation='h',
                    hoverinfo='x',
                    name= "Óbitos",
                    showlegend=True,
                    opacity=0.6,
                    marker=dict(color='black')
                    ))

        fig.add_trace(go.Bar(y=yidx,
                    x= -1 * mulheres_obito_paty_cons.to_numpy().flatten(),
                    orientation='h',
                    text= mulheres_obito_paty_cons.to_numpy().flatten().astype('int'),
                    hoverinfo='text',
                    showlegend=False,
                    opacity=0.6,
                    marker=dict(color='black')
                    ))

        fig.update_layout(barmode='overlay', 
                        autosize=True,
                        #height=500, 
                        #width=800, 
                        #yaxis_autorange='reversed',
                        yaxis_visible=False,
                        bargap=0.1,
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)'
                        )

        fig.update_layout(
            xaxis = dict(
                #tickmode = 'array',
                tickvals = [min(-1 * mulheres_contaminadas_paty_cons.to_numpy().flatten()),-10,-5,0,5,str(max(homens_contaminadas_paty_cons.to_numpy().flatten()))],
                ticktext = [str(max(mulheres_contaminadas_paty_cons.to_numpy().flatten())),'10','5','0','5',str(max(homens_contaminadas_paty_cons.to_numpy().flatten()))]
            )
        )


        return plot(fig, include_plotlyjs=True, output_type='div')


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

        grafico_piramide = self.getPopulationPyramidGraph()


        return render(request,"dashboard/cidades/paty/paty.html", context={'plot_div': trace,'bar_suspeitos': trace2, 'confirmados':confirmados,'curados':curados,'internados':internados,'obitos':obitos,'ultima_atu': ultima_atu,'plot_bar_sem':trace_casos_semanais, 'graf_piramide_paty':grafico_piramide})



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



