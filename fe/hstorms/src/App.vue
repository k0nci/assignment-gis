<template>
    <div id="app" class="container-fluid h-100">
        <div class="row h-100">
            <div class="col-3">
                <search-point class="border border-primary rounded mt-3 p-2"/>
                <country-heatmap class="border border-primary rounded mt-3 p-2"/>
            </div>
            <div class="col-9">
                <leaflet-map/>
            </div>
        </div>
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
</style>
