 # -*- coding: utf-8 -*-
import streamlit as st
#import gpxdf
import gpxpy
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static

def main():
    st.title('Map with GPX tracks')
    st.text('GPXファイルをアップロードすると、経路付きの地図を表示します。')

    uploaded_file = st.file_uploader("Choose a GPX file",type='gpx')
    if uploaded_file is not None:
        #st.write(uploaded_file)
        
        gpx_p = gpxpy.parse(uploaded_file.getvalue().decode('utf-8'))
        gpx_list = []
        # tonlist
        for track in gpx_p.tracks:
            for i, segment in enumerate(track.segments):
                for point in segment.points:
                    gpx_list.append([point.latitude, point.longitude,
                                    point.elevation, point.time, track.name, i])
        # to pd.DataFrame
        colname = ['latitude', 'longitude',
                'elevation', 'time', 'trackname', 'segment_no']
        df = pd.DataFrame(gpx_list, columns=colname)


        #with open('uploaded_gpx.gpx', mode='w') as f:
        #    f.write(bytes_data.decode('utf-8'))
        #df = gpxdf.read_gpx('uploaded_gpx.gpx')
        
        #fig = plt.figure(figsize=(12,9))
        #plt.plot(df.longitude, df.latitude)
        #st.pyplot(fig)
        #st.table(df.head())

        df_t = df[['latitude', 'longitude']]
        #st.map(df_t,zoom=8)

        map=folium.Map(location=(df_t.iloc[0]+df_t.iloc[-1])/2, zoom_start=10)
        folium.PolyLine(df_t).add_to(map)
        folium_static(map)

    st.text('※ファイルサイズが大きいとエラーになります。')

if __name__ == '__main__':
    main()