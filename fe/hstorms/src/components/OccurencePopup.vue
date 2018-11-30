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
                <b-badge variant="primary" pill>{{area}}</b-badge>
            </b-list-group-item>
        </b-list-group>
    </div>
</template>

<script>
    export default {
        name: "OccurencePopup",
        props: ['name', 'occurrence', 'area']
    }
</script>

<style scoped>

</style>