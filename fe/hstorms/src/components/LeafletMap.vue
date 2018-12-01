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
                            :options="hurricane.options"
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
            <div id="marker">
                <l-marker
                        v-if="marker.lat && marker.lon"
                        :lat-lng="[marker.lat, marker.lon]"
                        @click="unsetMarker"/>
                <l-circle
                        v-if="marker.lat && marker.lon && marker.distance > 0"
                        :lat-lng="[marker.lat, marker.lon]"
                        :radius="marker.distance"/>
            </div>
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
        LTileLayer,
        LCircle
    } from 'vue2-leaflet';
    import {mapGetters} from 'vuex';
    import {SET_MARKER, CLEAR_HUR_LAYERS} from '../store/mutations.type';
    import OccurrencePopup from './OccurencePopup';
    import HurricanePopop from './HurricanePopup';

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
            LMarker,
            LCircle
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
                default: 'https://api.mapbox.com/styles/v1/k0nci/cjp5vubh75a4m2sp6h17p8f7a/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiazBuY2kiLCJhIjoiY2pueG1pbW9iMGQ4aTNxbjc2dTV4NjRlNCJ9.UTeCfINkvmtamttjaBcvcA'
            },
            attribution: {
                type: String,
                default: '&copy; <a href=\'https://www.mapbox.com/about/maps/\'>Mapbox</a> &copy; <a href=\'http://www.openstreetmap.org/copyright\'>OpenStreetMap</a> <strong><a href=\'https://www.mapbox.com/map-feedback/\' target=\'_blank\'>Improve this map</a></strong>'
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
                },
                hurricane: {
                    options: {
                        onEachFeature(feature, layer) {
                            let PopupCont = Vue.extend(HurricanePopop);
                            let popup = new PopupCont({
                                propsData: {
                                    hurricaneId: feature.properties.hurricaneId,
                                    minDistance: feature.properties.minDistance
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
                this.$store.commit(CLEAR_HUR_LAYERS);
                this.$store.commit(SET_MARKER, {
                    lat: event.latlng.lat.toFixed(5),
                    lon: event.latlng.lng.toFixed(5)
                });
            },
            unsetMarker() {
                this.$store.commit(CLEAR_HUR_LAYERS);
                this.$store.commit(SET_MARKER, {});
            },
            hurricaneStyleFunction(feature) {
                return {
                    color: getHurricaneColor(feature.properties.status),
                    weight: 8
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

<style>
    @import '~leaflet/dist/leaflet.css';

    .leaflet-pane.leaflet-popup-pane {
        font-size: 1.3em;
    }
</style>