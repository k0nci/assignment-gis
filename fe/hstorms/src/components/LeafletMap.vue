<template>
    <div class="h-100">
        <l-map :zoom="zoom"
               :center="center"
               @click="setMarker">
            <l-control-layers/>
            <l-tile-layer :url="url"
                          :attribution="attribution"/>
            <l-geo-json v-for="(item, index) in hurricane_layers"
                        :key="index"
                        :geojson="item"
                        layer-type="overlay"/>
            <l-geo-json v-for="(item, index) in occurrence_layers"
                        :key="index"
                        :geojson="item"
                        :optionsStyle="occStyleFunction"
                        layer-type="overlay"/>
            <l-marker
                    v-if="marker.lat && marker.lon"
                    :lat-lng="[marker.lat, marker.lon]"
                    @click="unsetMarker"/>
        </l-map>
    </div>
</template>

<script>
    import {
        LControlLayers,
        LGeoJson,
        LMap,
        LMarker,
        LTileLayer
    } from 'vue2-leaflet';
    import {mapGetters} from 'vuex';
    import {SET_MARKER} from '../store/mutations.type';

    function getOccColor(occurrence) {
        switch (true) {
            case (occurrence > 105):
                return '#800026';
            case (occurrence > 65):
                return '#BD0026';
            case (occurrence > 40):
                return '#E31A1C';
            case (occurrence > 25):
                return '#FC4E2A';
            case (occurrence > 15):
                return '#FD8D3C';
            case (occurrence > 10):
                return '#FEB24C';
            case (occurrence > 5):
                return '#FED976';
            case (occurrence <= 5 && occurrence > 0):
                return '#FFEDA0';
            default:
                return '#FFFFFF';
        }
    }

    export default {
        name: 'LeafletMap',
        components: {
            LMap,
            LTileLayer,
            LGeoJson,
            LControlLayers,
            LMarker
        },
        props: {
            zoom: {
                type: Number,
                default: 5
            },
            center: {
                type: Array,
                default: () => [20.01, -75.49]
            },
            url: {
                type: String,
                default: 'https://cartodb-basemaps-{s}.global.ssl.fastly.net/rastertiles/voyager/{z}/{x}/{y}.png'
            },
            attribution: {
                type: String,
                default: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attribution">CARTO</a>'
            }
        },
        methods: {
            setMarker: function (event) {
                this.$store.commit(SET_MARKER, {
                    lat: event.latlng.lat,
                    lon: event.latlng.lng
                });
            },
            unsetMarker: function () {
                this.$store.commit(SET_MARKER, {});
            },
            occStyleFunction: function (feature) {
                return {
                    fillColor: getOccColor(feature.properties.occurrence),
                    weight: 2,
                    opacity: feature.properties.occurrence > 0 ? 1 : 0,
                    color: 'white',
                    dashArray: '3',
                    fillOpacity: 0.7
                };
            }
        },
        computed: {
            ...mapGetters(['hurricane_layers', 'marker', 'occurrence_layers'])
        }
    }
</script>

<style scoped>
    @import '~leaflet/dist/leaflet.css';
</style>