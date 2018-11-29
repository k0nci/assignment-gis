<template>
    <div class="h-100">
        <l-map :zoom="zoom"
               :center="center"
               @click="setMarker">
            <l-control-layers/>
            <l-tile-layer :url="url"
                          :attribution="attribution"/>
            <div id="hurricane_layers">
                <l-geo-json v-for="(item, index) in hurricane_layers"
                            :key="index"
                            :name="item.properties.name"
                            :geojson="item"
                            :optionsStyle="hurricaneStyleFunction"
                            layer-type="overlay"/>
            </div>
            <div id="occurrence_layers">
                <l-geo-json v-for="(item, index) in occurrence_layers"
                            :key="index"
                            :name="item.properties.countryName"
                            :geojson="item"
                            :options="occurrence.options"
                            :optionsStyle="occStyleFunction"
                            layer-type="overlay"/>
            </div>
            <l-marker
                    v-if="marker.lat && marker.lon"
                    :lat-lng="[marker.lat, marker.lon]"
                    @click="unsetMarker"/>
        </l-map>
    </div>
</template>

<script>
    import Vue from 'vue';
    import {
        LControlLayers,
        LGeoJson,
        LMap,
        LMarker,
        LTileLayer
    } from 'vue2-leaflet';
    import {mapGetters} from 'vuex';
    import {SET_MARKER} from '../store/mutations.type';
    import OccurrencePopup from './OccurencePopup';

    function getHurricaneColor(status) {
        switch (true) {
            case (status === 'EX'):
                return '#FED976';
            case (status === 'TD'):
                return '#FEB24C';
            case (status === 'TS'):
                return '#E31A1C';
            case (status === 'HU'):
                return '#800026';
            default:
                return '#FFEDA0';
        }
    }

    function getOccColor(occurrence) {
        switch (true) {
            case (occurrence > 7e-9):
                return '#800026';
            case (occurrence > 6e-9):
                return '#BD0026';
            case (occurrence > 5e-9):
                return '#E31A1C';
            case (occurrence > 4e-9):
                return '#FC4E2A';
            case (occurrence > 3e-9):
                return '#FD8D3C';
            case (occurrence > 2e-9):
                return '#FEB24C';
            case (occurrence > 1e-9):
                return '#FED976';
            case (occurrence <= 1e-9 && occurrence > 0):
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
        data() {
            return {
                occurrence: {
                    options: {
                        onEachFeature(feature, layer) {
                            let name = feature.properties.regionName
                                ? feature.properties.regionName
                                : feature.properties.countryName;

                            let PopupCont = Vue.extend(OccurrencePopup);
                            let popup = new PopupCont({
                                propsData: {
                                    name: name,
                                    occurrence: feature.properties.occurrence,
                                    area: feature.properties.area
                                }
                            });
                            layer.bindPopup(popup.$mount().$el);
                        }
                    }
                }
            }
        },
        methods: {
            setMarker(event) {
                this.$store.commit(SET_MARKER, {
                    lat: event.latlng.lat,
                    lon: event.latlng.lng
                });
            },
            unsetMarker() {
                this.$store.commit(SET_MARKER, {});
            },
            hurricaneStyleFunction(feature) {
                return {
                    color: getHurricaneColor(feature.properties.status)
                }
            },
            occStyleFunction(feature) {
                let occurrence = feature.properties.occurrence / feature.properties.area;
                return {
                    fillColor: getOccColor(occurrence),
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