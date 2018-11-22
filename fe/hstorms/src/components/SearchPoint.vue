<template>
    <div class="border border-primary mt-3 p-2">
        <div class="form-group row">
            <label for="latitude"
                   class="col-sm-2 col-form-label col-form-label-sm">Lat:</label>
            <div class="col-sm-10">
                <input type="text" class="form-control form-control-sm"
                       id="latitude" placeholder="latitude"
                       v-model="marker.lat" disabled>
            </div>
        </div>

        <div class="form-group row">
            <label for="longitude"
                   class="col-sm-2 col-form-label col-form-label-sm">Lon:</label>
            <div class="col-sm-10">
                <input type="text" class="form-control form-control-sm"
                       id="longitude" placeholder="longitude"
                       v-model="marker.lon" disabled>
            </div>
        </div>

        <button type="button" class="btn btn-primary"
                @click="search">Search
        </button>
    </div>
</template>

<script>
    import {mapGetters} from "vuex";
    import {FIND_CLOSEST_H} from "../store/actions.type";
    import {HurricaneService} from '@/common/api.service';

    export default {
        name: 'SearchPoint',
        computed: {
            ...mapGetters(['marker'])
        },
        methods: {
            search: function () {
                this.$store.dispatch(FIND_CLOSEST_H, this.marker);
            }
        }
    }
</script>

<style scoped>

</style>