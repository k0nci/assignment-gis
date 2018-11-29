<template>
    <div>
        <h4>{{name}}</h4>
        <ul class="list-group">
            <li class="list-group-item d-flex justify-content-between align-items-center">
                Hurricane occurrence:
                <span class="badge badge-primary badge-pill">{{occurrence}}</span>
            </li>
            <li class="list-group-item d-flex justify-content-between align-items-center">
                Area:
                <span class="badge badge-primary badge-pill">{{area}}</span>
            </li>
        </ul>
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