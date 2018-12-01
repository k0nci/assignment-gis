<template>
    <div>
        <h4>{{name}}</h4>
        <b-list-group>
            <b-list-group-item class="d-flex justify-content-between align-items-center">
                Hurricane occurrence:
                <b-badge variant="primary" pill>{{occurrence}}</b-badge>
            </b-list-group-item>
            <b-list-group-item class="d-flex justify-content-between align-items-center">
                Area:
                <b-badge variant="primary" pill>{{areaKm}} km<sup>2</sup></b-badge>
            </b-list-group-item>
        </b-list-group>
    </div>
</template>

<script>
    export default {
        name: "OccurencePopup",
        props: ['name', 'occurrence', 'area'],
        computed: {
            areaKm() {
                return (this.area / Math.pow(1000, 2)).toFixed(1);
            }
        }
    }
</script>

<style scoped>

</style>