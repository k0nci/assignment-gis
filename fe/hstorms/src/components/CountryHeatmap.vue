<template>
    <div>
        <h2 class="bg-primary text-white">Occurrence in country</h2>
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

                <b-row>
                    <b-col>
                        <b-button type="button" variant="primary"
                                  @click="search">Show
                        </b-button>
                    </b-col>
                    <b-col>
                        <b-button type="button" variant="danger"
                                  @click="clearOccurrence">Clear
                        </b-button>
                    </b-col>
                </b-row>
            </b-form>
        </div>
    </div>
</template>

<script>
    import {CountryService} from '../common/api.service';
    import {CLEAR_OCC_LAYERS} from '../store/mutations.type';
    import {COUNT_OCC_BY_COUNTRY} from '../store/actions.type';

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
                    country_id: this.selectedCountry
                });
            },
            clearOccurrence() {
                this.$store.commit(CLEAR_OCC_LAYERS);
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