<!-- This file is part of Happyschool. -->
<!--  -->
<!-- Happyschool is the legal property of its developers, whose names -->
<!-- can be found in the AUTHORS file distributed with this source -->
<!-- distribution. -->
<!--  -->
<!-- Happyschool is free software: you can redistribute it and/or modify -->
<!-- it under the terms of the GNU Affero General Public License as published by -->
<!-- the Free Software Foundation, either version 3 of the License, or -->
<!-- (at your option) any later version. -->
<!--  -->
<!-- Happyschool is distributed in the hope that it will be useful, -->
<!-- but WITHOUT ANY WARRANTY; without even the implied warranty of -->
<!-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the -->
<!-- GNU Affero General Public License for more details. -->
<!--  -->
<!-- You should have received a copy of the GNU Affero General Public License -->
<!-- along with Happyschool.  If not, see <http://www.gnu.org/licenses/>. -->

<template>
    <div>
        <b-container>
            <b-row>
                <h2>Dossier des élèves</h2>
            </b-row>
            <b-row>
                <b-col>
                    <b-form-group>
                        <div>
                            <b-btn variant="primary" @click="openDynamicModal('add-modal')">
                                <icon name="plus" scale="1" class="align-middle"></icon>
                                Nouveau cas
                            </b-btn>
                            <b-btn variant="outline-secondary" v-b-toggle.filters>
                                <icon name="search" scale="1"></icon>
                                Ajouter des filtres
                            </b-btn>
                        </div>
                    </b-form-group>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                        <b-collapse id="filters" v-model=showFilters>
                            <b-card>
                                <filters app="dossier_eleve" model="cas_eleve" ref="filters" @update="applyFilter"></filters>
                            </b-card>
                        </b-collapse>
                    </b-col>
            </b-row>
            <b-pagination class="mt-1" :total-rows="entriesCount" v-model="currentPage" @change="changePage" :per-page="20">
            </b-pagination>
            <b-card no-body class="current-card d-none d-md-block d-lg-block d-xl-block">
                <b-row class="text-center">
                    <b-col cols="2"><strong>Catégorie</strong></b-col>
                    <b-col><strong>Commentaire(s)</strong></b-col>
                </b-row>
            </b-card>
            <cas-eleve-entry
                v-for="(entry, index) in entries"
                v-bind:key="entry.id"
                v-bind:row-data="entry"
                @delete="askDelete(entry.id)"
                @edit="editEntry(index)"
                @filterStudent="filterStudent($event)"
                >
            </cas-eleve-entry>
            <b-modal ref="deleteModal" cancel-title="Annuler" hide-header centered @ok="deleteEntry">
                Êtes-vous sûr de vouloir supprimer définitivement cette entrée ?
            </b-modal>
            <component v-bind:is="currentModal" ref="dynamicModal" @update="loadEntries"></component>
        </b-container>
    </div>
</template>

<script>
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue'

import 'vue-awesome/icons'
import Icon from 'vue-awesome/components/Icon.vue'
Vue.component('icon', Icon);

import axios from 'axios';
window.axios = axios;
window.axios.defaults.baseURL = window.location.origin; // In order to have httpS.

import Filters from '../common/filters.vue'
import CasEleveEntry from './casEleveEntry.vue'
import AddModal from './addModal.vue'

export default {
    data: function () {
        return {
            entriesCount: 0,
            currentPage: 1,
            entries: [],
            currentEntry: -1,
            currentModal: 'add-modal',
            filter: "",
            ordering: "&ordering=-datetime_encodage",
            showFilters: false,
        }
    },
    methods: {
        changePage: function (page) {
            this.currentPage = page;
            this.loadEntries();
            return;
        },
        openDynamicModal: function (modal) {
            this.currentModal = modal;
            this.$refs.dynamicModal.show();
        },
        filterStudent: function (matricule) {
            this.showFilters = true;
            this.$store.commit('addFilter',
                {filterType: 'matricule_id', tag: matricule, value: matricule}
            );
            this.applyFilter()
        },
        applyFilter: function () {
            this.filter = "";
            let storeFilters = this.$store.state.filters
            console.log(storeFilters);
            for (let f in storeFilters) {
                if (storeFilters[f].filterType.startsWith("date")
                    || storeFilters[f].filterType.startsWith("time")) {
                    let ranges = storeFilters[f].value.split("_");
                    this.filter += "&" + storeFilters[f].filterType + "__gt=" + ranges[0];
                    this.filter += "&" + storeFilters[f].filterType + "__lt=" + ranges[1];
                } else {
                    this.filter += "&" + storeFilters[f].filterType + "=" + storeFilters[f].value;
                }
            }
            this.loadEntries();
        },
        askDelete: function (id) {
            this.currentEntry = id;
            this.$refs.deleteModal.show();
        },
        deleteEntry: function () {
            const token = { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
            axios.delete('/dossier_eleve/api/cas_eleve/' + this.currentEntry + '/', token)
            .then(response => {
                this.loadEntries();
            });
        },
        loadEntries: function () {
            axios.get('/dossier_eleve/api/cas_eleve/?page=' + this.currentPage + this.filter + this.ordering)
            .then(response => {
                this.entriesCount = response.data.count;
                this.entries = response.data.results;
            });
        },
    },
    mounted: function () {
        this.loadEntries();
    },
    components: {
        'filters': Filters,
        'cas-eleve-entry': CasEleveEntry,
        'add-modal': AddModal,
    }
}
</script>

<style>
</style>
