<template>
    <div id="app" class="container-fluid">
        <div class="row app-body">
            <div class="col-md-3">
                <!-- The layer checkboxes go here -->
            </div>
            <div class="col-md-9">
                <l-map
                        :zoom="zoom"
                        :center="center">
                    <l-tile-layer
                            :url="url"
                            :attribution="attribution"/>
                </l-map>
            </div>
        </div>
    </div>
</template>

<script>
    import {LMap, LTileLayer} from 'vue2-leaflet';

    export default {
        name: 'app',
        components: {
            LMap,
            LTileLayer,
            // LGeoJson
        },
        data() {
            return {
                zoom: 5,
                center: [20.01, -75.49],
                url: 'https://cartodb-basemaps-{s}.global.ssl.fastly.net/rastertiles/voyager/{z}/{x}/{y}.png',
                attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attribution">CARTO</a>'
            }
        }
    }
</script>

<style>
    @import "~leaflet/dist/leaflet.css";

    #app {
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
    }

    .app-body {
        margin: 1em;
        height: calc(100vh - 2em);
        overflow: auto;
    }
</style>
