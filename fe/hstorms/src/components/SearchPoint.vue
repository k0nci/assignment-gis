<template>
    <div>
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
            <div class="form-check">
                <input class="form-check-input" type="checkbox"
                       v-model="searchInDistance" id="searchDistance">
                <label class="form-check-label" for="searchDistance">
                    Search in distance
                </label>
            </div>
            <div class="form-group row">
                <label for="distance"
                       class="col-sm-3 col-form-label col-form-label-sm">Distance:</label>
                <div class="col-sm-9">
                    <input type="number" class="form-control form-control-sm"
                           id="distance" placeholder="distance"
                           v-model.number.lazy="distance"
                           :disabled="!searchInDistance">
                </div>
            </div>
        </div>

        <button type="button" class="btn btn-primary"
                @click="search">Search
        </button>
    </div>
</template>

<script>
    import {mapGetters} from 'vuex';
    import {FIND_BY_POINT} from '../store/actions.type';

    export default {
        name: 'SearchPoint',
        computed: {
            ...mapGetters(['marker'])
        },
        data() {
            return {
                searchInDistance: false,
                distance: undefined
            };
        },
        methods: {
            search: function () {
                if (this.searchInDistance) {
                    this.$store.dispatch(FIND_BY_POINT, {
                        ...this.marker,
                        distance: this.distance
                    });
                } else {
                    this.$store.dispatch(FIND_BY_POINT, this.marker);
                }
            }
        }
    }
</script>

<style scoped>

</style>