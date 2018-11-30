<template>
    <div id="app" class="h-100">
        <b-navbar type="light" variant="light">
            <b-navbar-brand>PDT - HSTORMS</b-navbar-brand>
        </b-navbar>
        <b-container class="h-100" fluid>
            <b-row class="h-100">
                <b-col lg="2">
                    <search-point
                            class="border border-primary rounded mt-3 p-2"/>
                    <country-heatmap
                            class="border border-primary rounded mt-3 p-2"/>
                </b-col>
                <b-col lg="10">
                    <leaflet-map/>
                </b-col>
            </b-row>
        </b-container>
    </div>
</template>

<script>
    import LeafletMap from './components/LeafletMap';
    import SearchPoint from './components/SearchPoint';
    import CountryHeatmap from './components/CountryHeatmap';

    export default {
        name: 'app',
        components: {
            LeafletMap,
            SearchPoint,
            CountryHeatmap
        }
    }
</script>

<style>

    #app {
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
    }

    html, body {
        height: 100%;
    }

    .leaflet-pane.leaflet-popup-pane {
        font-size: 1.3em;
    }
</style>
