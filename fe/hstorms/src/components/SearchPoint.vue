<template>
    <div>
        <h2>Search by point</h2>
        <span>Click on map to put marker</span>
        <form>
            <div class="form-group row">
                <label for="latitude"
                       class="col-sm-3 col-form-label col-form-label-sm">Lat:</label>
                <div class="col-sm-9">
                    <input type="text" class="form-control form-control-sm"
                           id="latitude" placeholder="latitude"
                           v-model="marker.lat" disabled>
                </div>
            </div>

            <div class="form-group row">
                <label for="longitude"
                       class="col-sm-3 col-form-label col-form-label-sm">Lon:</label>
                <div class="col-sm-9">
                    <input type="text" class="form-control form-control-sm"
                           id="longitude" placeholder="longitude"
                           v-model="marker.lon" disabled>
                </div>
            </div>

            <div class="form-group row">
                <label for="year"
                       class="col-sm-3 col-form-label col-form-label-sm">Year:</label>
                <div class="col-sm-9">
                    <input type="number" class="form-control form-control-sm"
                           id="year" placeholder="year"
                           min="1851" max="2017"
                           v-model.number.lazy="year">
                </div>
            </div>

            <div>
                <div class="form-group row">
                    <label for="distance"
                           class="col-sm-3 col-form-label col-form-label-sm">Distance:</label>
                    <div class="col-sm-9">
                        {{ distanceKm }}km
                        <!--<input type="number" class="form-control form-control-sm"-->
                        <!--id="distance" placeholder="distance"-->
                        <!--v-model.number.lazy="distance"-->
                        <!--:disabled="!searchInDistance">-->
                    </div>
                </div>
                <div class="ml-4 mr-4">
                    <input type="range" class="form-control-range"
                           id="distance"
                           min="0" max="1000000"
                           v-model.number="marker.distance">
                </div>
            </div>

            <div class="form-group row mt-3">
                <div class="col-sm-6">
                    <button type="button" class="btn btn-primary"
                            @click="search">Search
                    </button>
                </div>
                <div class="col-sm-6">
                    <button type="button" class="btn btn-primary"
                            @click="clearHurricanes">Clear
                    </button>
                </div>
            </div>
        </form>
    </div>
</template>

<script>
    import {mapGetters} from 'vuex';
    import {CLEAR_HUR_LAYERS} from "../store/mutations.type";
    import {FIND_BY_POINT} from '../store/actions.type';

    export default {
        name: 'SearchPoint',
        computed: {
            ...mapGetters(['marker', 'hurricane_layers']),
            distanceKm() {
                return (this.marker.distance/1000).toFixed(1);
            }
        },
        data() {
            return {
                year: ''
            }
        },
        methods: {
            search() {
                if (this.marker.lat && this.marker.lon) {
                    let request = {
                        lat: this.marker.lat,
                        lon: this.marker.lon
                    };

                    if (this.marker.distance !== 0) {
                        request.distance = this.marker.distance;
                    }

                    if (this.year !== '') {
                        request.year = this.year;
                    }

                    this.$store.dispatch(FIND_BY_POINT, request);
                }
            },
            clearHurricanes() {
                this.$store.commit(CLEAR_HUR_LAYERS);
            }
        }
    }
</script>

<style scoped>

</style>