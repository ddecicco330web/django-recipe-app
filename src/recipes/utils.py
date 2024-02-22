from io import BytesIO 
import base64
import matplotlib.pyplot as plt

# get_graph: Returns a base64 encoded image of the plot
def get_graph():
   buffer = BytesIO()         

   #create a plot with a bytesIO object as a file-like object. Set format to png
   plt.savefig(buffer, format='png')

   buffer.seek(0)

   #retrieve the content of the file
   image_png=buffer.getvalue()

   #encode the bytes-like object
   graph=base64.b64encode(image_png)

   #decode to get the string as output
   graph=graph.decode('utf-8')

   buffer.close()

   return graph

# get_charts: Returns a list of base64 encoded images of the bar, pie, and line charts
def get_charts(data, **kwargs):
    #switch plot backend to AGG (Anti-Grain Geometry) - to write to file
    plt.switch_backend('AGG')

    #specify figure size
    fig=plt.figure(figsize=(5,4))

    # get charts
    # add bar chart
    plt.bar(data['name'], data['cook_time'])
    plt.xlabel('Name')
    plt.ylabel('Cook Time (min)')
    plt.xticks(rotation=30)
    #specify layout details
    plt.tight_layout()
    charts = [get_graph()]

     # clear the figure
    plt.clf()

    # add pie chart
    labels=kwargs.get('labels')
    plt.pie(data['cook_time'], labels=labels)
    plt.legend(data['name'], loc='best') 
    plt.tight_layout()
    charts.append(get_graph())
    plt.clf()

    # add line chart
    plt.plot(data['name'], data['cook_time'])
    plt.xlabel('Name')
    plt.ylabel('Cook Time (min)')
    plt.xticks(rotation=30)
    plt.tight_layout()
    charts.append(get_graph())

    return charts
