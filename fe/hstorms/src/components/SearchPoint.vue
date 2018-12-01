<template>
    <div>
        <h2 class="bg-primary text-white">Search by point</h2>
        <div class="p-2">
            <span>Click on map to put marker</span>
            <b-form>
                <b-form-group :label-cols="3"
                              label="Lat:"
                              label-for="latitude"
                              horizontal>
                    <b-form-input type="text"
                                  id="latitude" placeholder="latitude"
                                  v-model="marker.lat" disabled></b-form-input>
                </b-form-group>

                <b-form-group :label-cols="3"
                              label="Lon:"
                              label-for="longitude"
                              horizontal>
                    <b-form-input type="text"
                                  id="longitude" placeholder="longitude"
                                  v-model="marker.lon" disabled></b-form-input>
                </b-form-group>

                <b-form-group :label-cols="3"
                              label="Year:"
                              label-for="year"
                              horizontal>
                    <b-form-input type="number"
                                  id="year" placeholder="year"
                                  min="1851" max="2017"
                                  v-model.number.lazy="year"></b-form-input>
                </b-form-group>

                <div>
                    <div class="form-group row">
                        <label for="distance"
                               class="col-sm-3 col-form-label col-form-label-sm">Distance:</label>
                        <div class="col-sm-9">
                            {{ distanceKm }}km
                        </div>
                    </div>
                    <div class="ml-4 mr-4">
                        <input type="range" class="form-control-range"
                               id="distance"
                               min="0" max="1000000"
                               v-model.number="marker.distance">
                    </div>
                </div>

                <b-row class="mt-3">
                    <b-col>
                        <b-button type="button" variant="primary"
                                  @click="search">Search
                        </b-button>
                    </b-col>
                    <b-col>
                        <b-button type="button" variant="danger"
                                  @click="clearHurricanes">Clear
                        </b-button>
                    </b-col>
                </b-row>
            </b-form>
        </div>
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
                return (this.marker.distance / 1000).toFixed(1);
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