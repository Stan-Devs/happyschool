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
        <div class="loading" v-if="!loaded"></div>
        <b-container v-if="loaded">
            <h1>Annuaire</h1>
            <b-row>
                <b-col md="2" sm="12">
                    <b-form-group label="Enseignement(s) :">
                        <b-form-select
                            multiple
                            :select-size="3"
                            v-model="teachings"
                            :options="teachingsOptions"
                            value-field="id"
                            text-field="display_name"
                            >
                        </b-form-select>
                    </b-form-group>
                </b-col>
                <b-col>
                    <b-form-group label="Recherche :" class="ml-4">
                        <multiselect id="input-name"
                            :internal-search="false"
                            :options="searchOptions"
                            @search-change="getSearchOptions"
                            :loading="searchLoading"
                            placeholder="Rechercher un étudiant, une classe, un professeur, …"
                            select-label=""
                            selected-label="Sélectionné"
                            deselect-label=""
                            label="display"
                            track-by="id"
                            v-model="search"
                            @select="selected"
                            >
                            <span slot="noResult">Aucune personne trouvée.</span>

                        </multiselect>
                    </b-form-group>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                    <b-list-group class="text-center">
                        <b-list-group-item v-for="s in students" :key="s.matricule"
                            button @click="selectStudent(s.matricule)"
                            >
                            {{ s.display }}
                        </b-list-group-item>
                    </b-list-group>
                </b-col>
            </b-row>
            <info v-if="matricule && students.length == 0" :matricule="matricule" :type="type" last_news></info>
        </b-container>
    </div>
</template>

<script>
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue'

import Multiselect from 'vue-multiselect'
import 'vue-multiselect/dist/vue-multiselect.min.css'

import 'vue-awesome/icons'
import Icon from 'vue-awesome/components/Icon.vue'
Vue.component('icon', Icon);

import axios from 'axios';

import Info from './info.vue';

export default {
    data: function () {
        return {
            loaded: false,
            searchId: 0,
            teachings: [],
            teachingsOptions: [],
            search: null,
            searchOptions: [],
            searchLoading: false,
            students: [],
            type: null,
            matricule: null,
        }
    },
    methods: {
        selected: function (option) {
            if (option.type == 'classe') {
                const data = {params: {classe: option.id}};
                axios.get('/annuaire/api/studentclasse/', data)
                .then(response => {
                    this.students = response.data;
                })
                return;
            } else {
                this.students = [];
                this.matricule = option.id;
                this.type = option.type;
            }
        },
        selectStudent: function (matricule) {
            this.matricule = matricule;
            this.students = [];
            this.type = 'student';
        },
        getSearchOptions: function (query) {
            // Ensure the last search is the first response.
            this.searchId += 1;
            let currentSearch = this.searchId;

            const token = { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
            const data = {
                query: query,
                teachings: this.teachings.length > 0 ? this.teachings : this.teachingsOptions.map(t => t.id),
                people: 'all',
                check_access: false,
            };
            axios.post('/annuaire/api/people_or_classes/', data, token)
            .then(response => {
                if (this.searchId !== currentSearch)
                    return;

                const options = response.data.map(p => {
                    if (Number.isNaN(Number.parseInt(query[0]))) {
                        // It is a student or a responsible.
                        if ('is_secretary' in p) {
                            // It is a responsible.
                            let teachings = " —";
                            for (let t in p.teaching) {
                                teachings += " " + p.teaching[t].display_name;
                            }

                            return {
                                display: p.last_name + ' ' + p.first_name + teachings,
                                id: p.matricule,
                                type: 'responsible',
                            };
                        } else {
                            // It is a student.
                            return {
                                display: p.display,
                                id: p.matricule,
                                type: 'student',
                            }
                        }
                    } else {
                        // It is a classe.
                        let classe = p;
                        classe.type = 'classe';
                        return classe;
                    }
                })

                this.searchOptions = options;
            });
        },
        changeComponent: function (component) {
            this.currentComponent = component;
        }
    },
    mounted: function () {
        axios.get('/core/api/teaching/')
        .then(response => {
            this.teachingsOptions = response.data.results;
            this.loaded = true;
        });
    },
    components: {
        'multiselect': Multiselect,
        'info': Info,
    }
}
</script>

<style>
.loading {
  content: " ";
  display: block;
  position: absolute;
  width: 80px;
  height: 80px;
  background-image: url(/static/img/spin.svg);
  background-size: cover;
  left: 50%;
  top: 50%;
}
</style>
