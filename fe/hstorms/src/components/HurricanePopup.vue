<template>
    <div>
        <h4>{{ hurricane.name }}</h4>
        <ul class="list-group">
            <li class="list-group-item d-flex justify-content-between align-items-center">
                Hurricane length:
                <span class="badge badge-primary badge-pill">{{ hurricane.hurricaneLength }} km</span>
            </li>
            <li class="list-group-item d-flex justify-content-between align-items-center">
                Start date:
                <span class="badge badge-primary badge-pill">{{ hurricane.startDate }}</span>
            </li>
            <li class="list-group-item d-flex justify-content-between align-items-center">
                End date:
                <span class="badge badge-primary badge-pill">{{ hurricane.endDate }}</span>
            </li>
        </ul>
    </div>
</template>

<script>
    import {HurricaneService} from '../common/api.service';

    export default {
        name: "HurricanePopup",
        props: ['hurricaneId'],
        data() {
            return {
                hurricane: {
                    name: undefined,
                    hurricaneLength: undefined,
                    startDate: undefined,
                    endDate: undefined
                }
            }
        },
        mounted() {
            HurricaneService.query('info', {
                hurricaneId: this.hurricaneId
            }).then(response => {
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