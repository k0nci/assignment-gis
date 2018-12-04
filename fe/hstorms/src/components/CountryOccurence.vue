<template>
    <div>
        <h2>Occurrence in country</h2>
        <div class="p-2">
            <b-form>
                <b-form-group label="Select country"
                              label-for="countrySelect">
                    <b-form-select
                            id="contrySelect"
                            v-model="selectedCountry"
                            :options="countries">
                    </b-form-select>
                </b-form-group>

                <b-button type="button" variant="primary"
                          @click="search">Show
                </b-button>

            </b-form>
        </div>
    </div>
</template>

<script>
    import {CountryService} from '../common/api.service';
    import {COUNT_OCC_BY_COUNTRY} from '../store/actions.type';

    export default {
        name: 'CountryOccurence',
        data() {
            return {
                selectedCountry: undefined,
                countries: []
            }
        },
        methods: {
            search() {
                this.$store.dispatch(COUNT_OCC_BY_COUNTRY, {
                    countryId: this.selectedCountry
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