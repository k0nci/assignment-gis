<template>
    <div>
        <div class="form-group">
            <label for="contrySelect">Select country</label>
            <select class="form-control"
                    id="contrySelect"
                    v-model="selectedCountry">
                <option v-for="(item, index) in countries"
                        :key="index"
                        :value="item.ids">
                    {{ item.name }}
                </option>
            </select>
        </div>
        <button type="button" class="btn btn-primary"
                @click="search">Show
        </button>
    </div>
</template>

<script>
    import {CountryService} from '../common/api.service';
    import {COUNT_OCC_BY_COUNTRY} from "../store/actions.type";

    export default {
        name: 'CountryHeatmap',
        data() {
            return {
                selectedCountry: undefined,
                countries: []
            }
        },
        methods: {
            search() {
                this.$store.dispatch(COUNT_OCC_BY_COUNTRY, {
                    country_ids: this.selectedCountry
                });
            }
        },
        mounted() {
            CountryService.get()
                .then(response => {
                    this.countries = response.data
                });
        }
    }
</script>

<style scoped>

</style>