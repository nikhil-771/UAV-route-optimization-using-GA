import folium
from variables import waypoints

def get_legend_html():
    return '''
        <div style="
            position: fixed; 
            bottom: 50px; 
            left: 50px; 
            z-index: 1000;
            background: white;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.3);
            font-family: Arial;
            font-size: 14px;
            ">
            <div style="display: flex; align-items: center; margin: 5px 0;">
                <div style="
                    background: #4CAF50; 
                    width: 20px; 
                    height: 20px; 
                    border-radius: 50%; 
                    margin-right: 10px;
                    border: 1px solid #2E7D32">
                </div>
                Start Point
            </div>
            <div style="display: flex; align-items: center; margin: 5px 0;">
                <div style="
                    background: #EF5350; 
                    width: 20px; 
                    height: 20px; 
                    border-radius: 50%; 
                    margin-right: 10px;
                    border: 1px solid #C62828">
                </div>
                End Point
            </div>
        </div>
    '''

def plot_initial_waypoints(waypoints, name):
    map_center = waypoints[0]
    m = folium.Map(location=map_center, zoom_start=13)

    for i, waypoint in enumerate(waypoints):
        if i == 0:
            folium.Marker(location=waypoint, popup="Start", icon=folium.Icon(color='green')).add_to(m)
        elif i == len(waypoints) - 1:
            folium.Marker(location=waypoint, popup="Final", icon=folium.Icon(color='red')).add_to(m)
        else:
            folium.Marker(location=waypoint, popup=f"Waypoint {i}", icon=folium.Icon(color='blue')).add_to(m)

    # Add invisible polyline to fix legend rendering
    folium.PolyLine([waypoints[0], waypoints[-1]], color='white', opacity=0).add_to(m)

    # Add legend
    m.get_root().html.add_child(folium.Element(get_legend_html()))

    m.save(name + '.html')
    print(f"Waypoints added to the map named '{name}.html'")

def plot_final_waypoints(waypoints, name):
    m = folium.Map(location=waypoints[0], zoom_start=13)
    folium.PolyLine(waypoints, color="blue", weight=2.5, opacity=1).add_to(m)

    for i, waypoint in enumerate(waypoints):
        if i == 0:
            popup_text = "Start"
            icon_color = "green"
        elif i == len(waypoints) - 1:
            popup_text = "Final"
            icon_color = "red"
        else:
            popup_text = f"Waypoint {i}"
            icon_color = "blue"

        folium.Marker(location=waypoint, popup=popup_text, icon=folium.Icon(color=icon_color)).add_to(m)

        folium.map.Marker(
            location=waypoint,
            icon=folium.DivIcon(html=f"""<div style="font-size: 12pt; color: black"><b>{i}</b></div>""")
        ).add_to(m)

    # Add legend
    m.get_root().html.add_child(folium.Element(get_legend_html()))

    m.save(name + '.html')
    print(f"Final map with best route generated as '{name}.html'")
