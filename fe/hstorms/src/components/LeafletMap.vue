<template>
    <div class="h-100">
        <l-map :zoom="zoom"
               :center="center"
               @click="setMarker">
            <l-control-layers/>
            <l-tile-layer :url="url"
                          :attribution="attribution"/>
            <l-geo-json v-for="(item, index) in geojson_layers"
                        :key="index"
                        :geojson="item"
                        layer-type="overlay"/>
            <l-marker
                    v-if="marker.lat !== undefined && marker.lon !== undefined"
                    :lat-lng="[marker.lat, marker.lon]"/>
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
                })
            }
        },
        computed: {
            ...mapGetters(['geojson_layers', 'marker'])
        }
    }
</script>

<style scoped>
    @import '~leaflet/dist/leaflet.css';
</style>