<template>
    <div>
        <b-button class="w-100" type="button" variant="danger"
                  @click="clearLayers">Clear map
        </b-button>
        <search-point
                class="menu mt-3"/>
        <country-occurence
                class="menu mt-3"/>
    </div>
</template>

<script>
    import SearchPoint from './SearchPoint';
    import CountryOccurence from './CountryOccurence';
    import {CLEAR_LAYERS} from '../store/actions.type';

    export default {
        name: "SideNavMenu",
        components: {
            SearchPoint,
            CountryOccurence
        },
        methods: {
            clearLayers() {
                this.$store.dispatch(CLEAR_LAYERS);
            }
        }
    }
</script>

<style scoped>

    .menu {
        border: 2px solid #007bff;
        border-radius: 5px;
    }

    .menu >>> h2 {
        background: #007bff;
        color: white;
        font-size: 1.5em;
        padding-bottom: 0.25em;
    }

</style>