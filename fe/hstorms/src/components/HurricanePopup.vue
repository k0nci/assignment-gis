<template>
    <div>
        <h4>{{ hurricane.name }}</h4>
        <b-list-group>
            <b-list-group-item
                    class="d-flex justify-content-between align-items-center">
                Minimal distance:
                <b-badge variant="primary" pill>
                    {{ minDistanceKm }} km
                </b-badge>
            </b-list-group-item>
            <b-list-group-item
                    class="d-flex justify-content-between align-items-center">
                Hurricane length:
                <b-badge variant="primary" pill>
                    {{ hurricane.hurricaneLength }} km
                </b-badge>
            </b-list-group-item>
            <b-list-group-item
                    class="d-flex justify-content-between align-items-center">
                Start date:
                <b-badge variant="primary" pill>
                    {{ hurricane.startDate }}
                </b-badge>
            </b-list-group-item>
            <b-list-group-item
                    class="d-flex justify-content-between align-items-center">
                End date:
                <b-badge variant="primary" pill>
                    {{ hurricane.endDate }}
                </b-badge>
            </b-list-group-item>
        </b-list-group>
    </div>
</template>

<script>
    import {HurricaneService} from '../common/api.service';

    export default {
        name: "HurricanePopup",
        props: ['hurricaneId', 'minDistance'],
        data() {
            return {
                hurricane: {
                    name: undefined,
                    hurricaneLength: undefined,
                    startDate: undefined,
                    endDate: undefined,

                }
            }
        },
        computed: {
            minDistanceKm() {
                return (this.minDistance / 100).toFixed(1);
            }
        },
        mounted() {
            HurricaneService.get(`${this.hurricaneId}/info`)
                .then(response => {
                    this.hurricane = response.data;
                    this.hurricane.hurricaneLength /= 1000;
                    this.hurricane.hurricaneLength = this.hurricane
                        .hurricaneLength.toFixed(1)
                });
        }
    }
</script>

<style scoped>

</style>