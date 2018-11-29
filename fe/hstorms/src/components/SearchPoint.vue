<template>
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

        <div>
            <div class="form-group row">
                <label for="distance"
                       class="col-sm-3 col-form-label col-form-label-sm">Distance:</label>
                <div class="col-sm-9">
                    <input type="range" class="form-control-range"
                           id="distance"
                           min="0" max="50000"
                           v-model.number="marker.distance">
                    <!--<input type="number" class="form-control form-control-sm"-->
                    <!--id="distance" placeholder="distance"-->
                    <!--v-model.number.lazy="distance"-->
                    <!--:disabled="!searchInDistance">-->
                </div>
                {{ (marker.distance/1000).toFixed(1) }}km
            </div>
        </div>

        <button type="button" class="btn btn-primary"
                @click="search">Search
        </button>
    </form>
</template>

<script>
    import {mapGetters} from 'vuex';
    import {FIND_BY_POINT} from '../store/actions.type';

    export default {
        name: 'SearchPoint',
        computed: {
            ...mapGetters(['marker'])
        },
        methods: {
            search() {
                if (this.marker.lat && this.marker.lon) {
                    if (this.marker.distance === 0) {
                        this.$store.dispatch(FIND_BY_POINT, {
                            lat: this.marker.lat,
                            lon: this.marker.lon
                        });
                    } else {
                        this.$store.dispatch(FIND_BY_POINT, this.marker);
                    }
                }
            }
        }
    }
</script>

<style scoped>

</style>