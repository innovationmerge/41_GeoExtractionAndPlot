import geograpy
import pandas as pd
import json
import plotly.express as px

text = "Bangalore(Bengaluru), is the capital of the Indian state of Karnataka. It has a population of about 10 million and a metropolitan population of about 8.52 million, making it the third most populous city and fifth most populous urban agglomeration in India."
#ext = "It took its present shape in 1956, when the former states of Mysore and Coorg were merged with the Kannada-speaking districts of the former states of Bombay, Hyderabad, and Madras. Unified Mysore state was made up of ten districts, Bangalore, Kolar, Tumakuru, Mandya, Mysore, Hassan, Chikkamagaluru , Shimoga, Chitradurga, and Ballari had been transferred from Madras state to Mysore in 1953, when the new state of Andhra Pradesh was created out of Madras' northern districts.[1] Coorg State became a district known as Kodagu,[2] Dakshina Kannada was transferred from Madras State, Uttara Kannada, Dharwad, Belgaum, and Viyapura from Bombay State. Bidar, Gulbarga, and Raichuru from Hyderabad State. It received its new name of Karnataka in the year 1973."

def getGeoGraphy(text):
    places = geograpy.get_place_context(text=text)
    return places.countries,places.regions,places.cities

def plotCities(detectedRegions,detectedCities):
    #check if state detected is Karnataka
    if 'Karnataka' in detectedRegions:
        #Read Karnataka GeoJSON
        with open('karnataka_district.json') as response:
            counties = json.load(response)
        #Read All the state information of Karnataka
        df = pd.read_csv("Karnataka.csv", dtype={"district": str})
        plotData = {}
        cities = []
        count = []
        #Check if detected city is part of karnataka
        for city in detectedCities:
            if len(df['district'].str.contains(city))>0:
                cities.append(city)
                count.append('1')
            else:
                pass
        #Create plotting data      
        plotData.update({"city":cities,'count':count})
        plotDf = pd.DataFrame(plotData, columns = ['city','count'])
        #Plot Map          
        fig = px.choropleth(plotDf, geojson=counties, 
                            color="count",
                            locations="city", 
                            featureidkey="properties.district",
                            projection="mercator",
                            color_continuous_scale="reds",
                            range_color=(0, 10))

        fig.update_geos(fitbounds="locations", visible=False)                          
        fig.update_layout(title="Identified City",
                            font=dict(family="Courier New, monospace",
                            size=30,
                            color="RebeccaPurple"))
        return fig    
        
def plotRegions(detectedRegions,detectedCities):
    if 'Karnataka' in detectedRegions:
        with open('karnataka_district.json') as response:
            counties = json.load(response)
        df = pd.read_csv("Karnataka.csv", dtype={"district": str})
        df1=df.copy()
        for city in detectedCities:
            try:
                index = int(df.loc[df.district == city].index[0])
                df1.at[index,'count'] = 10
            except:
                pass
        fig = px.choropleth(df1, geojson=counties, 
                            color="count",
                            locations="district", 
                            featureidkey="properties.district",
                            projection="mercator",
                            color_continuous_scale="Viridis",
                            range_color=(0, 10))

        fig.update_geos(fitbounds="locations", visible=False)                          
        fig.update_layout(title="Identified State and Regions",
                            font=dict(family="Courier New, monospace",
                            size=30,
                            color="RebeccaPurple"))

        return fig 
    
def plotCountry(detectedCountry,detectedRegions):
    if 'India' in detectedCountry:
        with open('indiaGeoJson.json') as response:
            geojson = json.load(response)
        df = pd.read_csv("India.csv", dtype={"state": str})
        df1=df.copy()
        for state in detectedRegions:
            try:
                index = int(df.loc[df.state == state].index[0])
                df1.at[index,'count'] = 10
            except:
                pass
        fig = px.choropleth(df1, geojson=geojson, 
                            color="count",
                            locations="state",
                            featureidkey="properties.ST_NM",
                            projection="mercator",
                            color_continuous_scale="Viridis",
                            range_color=(0, 10))
        fig.update_geos(fitbounds="locations", visible=False)                          
        fig.update_layout(title="Identified Country and State",
                            font=dict(family="Courier New, monospace",
                            size=30,
                            color="RebeccaPurple"))
        return fig     


if __name__ == "__main__":
    detectedCountry,detectedRegions,detectedCities=getGeoGraphy(text)
    plotCities(detectedRegions,detectedCities).show()   
    plotRegions(detectedRegions,detectedCities).show()
    plotCountry(detectedCountry,detectedRegions).show()
    print("places.countries", detectedCountry)
    print("places.regions",detectedRegions)
    print("places.cities",detectedCities)

