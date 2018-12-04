<template>
    <div id="app" class="h-100">
        <b-navbar type="light" variant="primary">
            <b-navbar-brand class="text-white">PDT - HSTORMS</b-navbar-brand>
        </b-navbar>
        <b-container class="app-container" fluid>
            <b-row class="h-100">
                <b-col lg="2">
                    <side-nav-menu class="mt-3"/>
                </b-col>
                <b-col lg="10">
                    <leaflet-map/>
                </b-col>
            </b-row>
        </b-container>
    </div>
</template>

<script>
    import LeafletMap from './components/LeafletMap';
    import SideNavMenu from './components/SideNavMenu';

    export default {
        name: 'app',
        components: {
            LeafletMap,
            SideNavMenu,
        }
    }
</script>

<style>
    #app {
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
    }

    html, body {
        height: 100%;
    }

    .leaflet-pane.leaflet-popup-pane {
        font-size: 1.3em;
    }

    .app-container {
        height: calc(100vh - 4em);
    }

</style>
