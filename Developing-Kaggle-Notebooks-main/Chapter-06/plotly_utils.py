import pandas as pd
import plotly.graph_objs as go
import plotly.figure_factory as ff
from plotly import tools
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)

def plotly_barplot(df, x_feature, y_feature, col, x_label, y_label, title):
    """
    Plot a barplot with number of y for category x
    Args:
        df: dataframe
        x_feature: x feature
        y_feature: y feature
        col: color for markers
        x_label: x label
        y_label: y label
        title: title
        
    Returns:
        None
    """
    trace = go.Bar(
            x = df[x_feature],
            y = df[y_feature],
            marker=dict(color=col),
            #text=df['location']
        )
    data = [trace]

    layout = dict(title = title,
              xaxis = dict(title = x_label, showticklabels=True, tickangle=15), 
              yaxis = dict(title = y_label),
              hovermode = 'closest'
             )
    fig = dict(data = data, layout = layout)
    iplot(fig, filename=f'images-{x_feature}-{y_feature}')
    
def plotly_heatmap(df, x_feature, y_feature, z_feature, x_label, y_label, title):
    """
    Plot a heatmap for x_feature x y_feature (z_feature)
        Args:
        df: dataframe
        x_feature: x feature
        y_feature: y feature
        z_feature: z feature
        x_label: x label
        y_label: y label
        title: title
        
    Returns:
        None
    """
    piv = pd.pivot_table(df, values=z_feature,index=[y_feature], columns=[x_feature], fill_value=0)
    m = piv.values
    trace = go.Heatmap(z = m, y= list(piv.index), x=list(piv.columns),colorscale='Rainbow',reversescale=False)
    data=[trace]
    layout = dict(title = title,
                  xaxis = dict(title = x_label,
                            showticklabels=True,
                               tickangle = 45,
                            tickfont=dict(
                                    size=10,
                                    color='black'),
                              ),
                  yaxis = dict(title = y_label, 
                            showticklabels=True, 
                               tickangle = 45,
                            tickfont=dict(
                                size=10,
                                color='black'),
                          ), 
                  hovermode = 'closest',
                  showlegend=False,
                      width=600,
                      height=600,
                 )
    fig = dict(data = data, layout = layout)
    iplot(fig, filename=f'images-{x_feature}-{y_feature}')

    
def plotly_sankey(df,cat_cols=[],value_cols='',title='Sankey Diagram', color_palette=None, height=None):
    """
    Plot a Sankey diagram
    Args:
        df: dataframe with data
        cat_cals: grouped by features
        valie_cols: feature grouped on
        title: graph title
        color_palette: list of colors
        height: graph height
    Returns:
        figure with the Sankey diagram
    
    """
    # maximum of 6 value cols -> 6 colors
    colorPalette = color_palette
    labelList = []
    colorNumList = []
    for catCol in cat_cols:
        labelListTemp =  list(set(df[catCol].values))
        colorNumList.append(len(labelListTemp))
        labelList = labelList + labelListTemp
        
    # remove duplicates from labelList
    labelList = list(dict.fromkeys(labelList))
    
    # define colors based on number of levels
    colorList = []
    for idx, colorNum in enumerate(colorNumList):
        colorList = colorList + [colorPalette[idx]]*colorNum
       
    # transform df into a source-target pair
    for i in range(len(cat_cols)-1):
        if i==0:
            sourceTargetDf = df[[cat_cols[i],cat_cols[i+1],value_cols]]
            sourceTargetDf.columns = ['source','target','count']
        else:
            tempDf = df[[cat_cols[i],cat_cols[i+1],value_cols]]
            tempDf.columns = ['source','target','count']
            sourceTargetDf = pd.concat([sourceTargetDf,tempDf])
        sourceTargetDf = sourceTargetDf.groupby(['source','target']).agg({'count':'sum'}).reset_index()
        
    # add index for source-target pair
    sourceTargetDf['sourceID'] = sourceTargetDf['source'].apply(lambda x: labelList.index(x))
    sourceTargetDf['targetID'] = sourceTargetDf['target'].apply(lambda x: labelList.index(x))
    
    # creating the sankey diagram
    data = dict(
        type='sankey',
        node = dict(
          pad = 15,
          thickness = 20,
          line = dict(
            color = "black",
            width = 0.5
          ),
          label = labelList,
          color = colorList
        ),
        link = dict(
          source = sourceTargetDf['sourceID'],
          target = sourceTargetDf['targetID'],
          value = sourceTargetDf['count']
        )
      )
    
    layout =  dict(
        title = title,
        font = dict(
          size = 10
        ),
        height=height
    )
       
    fig = dict(data=[data], layout=layout)
    return fig