<template>
    <div>
        <h2>Search by point</h2>
        <div class="pl-2 pr-2 pb-2">
            <div class="mb-3">
                <span>Click on map to put marker</span>
            </div>
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
                    <b-form-group :label-col="3"
                                  label="Distance:"
                                  horizontal>
                        <div class="ml-2 mr-2">
                            <input type="range" class="form-control-range"
                                   id="distance"
                                   min="0" max="1000000"
                                   v-model.number="marker.distance">
                        </div>
                        {{ distanceKm }}km
                    </b-form-group>
                </div>

                <b-button class="mt-3" type="button" variant="primary"
                          @click="search">Search
                </b-button>

            </b-form>
        </div>
    </div>
</template>

<script>
    import {mapGetters} from 'vuex';
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
            }
        }
    }
</script>

<style scoped>

</style>