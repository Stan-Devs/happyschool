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
    <b-modal size="lg" title="Nouveau cas"
        ok-title="Soumettre" cancel-title="Annuler"
        ref="addModal"
        @ok="addCas" @hidden="resetModal"
        >
        <b-row>
            <b-col sm="4">
                <div>
                    <b-img rounded :src="photoPath" fluid alt="Responsive image" />
                </div>
            </b-col>
            <b-col>
                <b-form>
                    <b-form-row>
                        <b-col sm="8">
                            <b-form-group label="Nom" label-for="input-name" :state="inputStates.name">
                                <multiselect id="input-name"
                                    :internal-search="false"
                                    :options="nameOptions"
                                    @search-change="getNameOptions"
                                    :loading="nameLoading"
                                    placeholder="Rechercher une personne…"
                                    select-label=""
                                    selected-label="Sélectionné"
                                    deselect-label=""
                                    label="display"
                                    track-by="matricule"
                                    v-model="name"
                                    >
                                    <span slot="noResult">Aucune personne trouvée.</span>

                                </multiselect>
                                <span slot="invalid-feedback">{{ errorMsg('name') }}</span>
                            </b-form-group>
                        </b-col>
                        <b-col sm="4">
                            <b-form-group label="Matricule" label-for="input-matricule">
                                <b-form-input id="input-matricule" type="text" v-model="name.matricule" readonly></b-form-input>
                            </b-form-group>
                        </b-col>
                    </b-form-row>
                    <b-form-row>
                        <b-col>
                            <b-form-group label="Objet" label-for="input-object" :state="inputStates.object_id">
                                <b-form-select id="input-object" v-model="form.object_id" :options="objectOptions">
                                    <template slot="first">
                                        <option :value="null" disabled>Choisissez un objet</option>
                                    </template>
                                </b-form-select>
                                <span slot="invalid-feedback">{{ errorMsg('object_id') }}</span>
                            </b-form-group>
                        </b-col>
                    </b-form-row>
                    <b-form-row>
                        <b-col>
                            <b-form-group label="Commentaires" label-for="input-comment">
                                <b-form-textarea id="input-comment" :rows="3" v-model="form.commentaire"></b-form-textarea>
                            </b-form-group>
                        </b-col>
                    </b-form-row>
                </b-form>
            </b-col>
        </b-row>
    </b-modal>
</div>
</template>

<script>
import Multiselect from 'vue-multiselect'
import 'vue-multiselect/dist/vue-multiselect.min.css'

import Moment from 'moment';
Moment.locale('fr');

import axios from 'axios';
window.axios = axios;
window.axios.defaults.baseURL = window.location.origin; // In order to have httpS.

export default {
    data: function () {
        return {
            form: {
                name: "",
                matricule_id: null,
                info_id: null,
                sanction_decision_id: null,
                commentaire: "",
                is_important: false,
                demandeur: "",
                visible_by_educ: true,
                visible_by_tenure: false,
            },
            timeMotifStart: null,
            timeMotifEnd: null,
            timeAppel: null,
            infoOptions: [],
            sanctionDecisionOptions: [],
            name: {matricule: null},
            nameOptions: [],
            nameLoading: false,
            searchId: 0,
            errors: {},
            inputStates: {
                name: null,
                info_id: null,
                sanction_decision_id: null,
                demandeur: null,
            }
        };
    },
    computed: {
        photoPath: function () {
            //TODO photo path
            return "/static/photos/4721.jpg";
        }
    },
    watch: {
        name: function () {
            // Update form data.
            if (this.name.matricule) {
                // First update form name data.
                this.form.name = this.name.display;
                if (this.name.matricule < 10000 && this.name.matricule > 999) {
                    // Student.
                    this.form.matricule_id = this.name.matricule;
                } else {
                    this.form.matricule_id = null;
                }
            }
        },
        errors: function (newErrors, oldErrors) {
            let inputs = ['name', 'info_id', 'sanction_decision_id', 'demandeur',];
            for (let u in inputs) {
                if (inputs[u] in newErrors) {
                    this.inputStates[inputs[u]] = newErrors[inputs[u]].length == 0;
                } else {
                    this.inputStates[inputs[u]] = null;
                }
            }
        }
    },
    methods: {
        show: function () {
            this.$refs.addModal.show();
        },
        hide: function () {
            this.$refs.addModal.hide();
        },
        resetModal: function () {
            //TODO resetModal()
        },
        errorMsg(err) {
            if (err in this.errors) {
                return this.errors[err][0];
            } else {
                return "";
            }
        },
        addAppel: function (evt) {
            evt.preventDefault();

            let data = this.form;
            // Add times if any.
            let time = this.timeMotifStart ? " " + this.timeMotifStart : " 12:00";
            data.datetime_motif_start += time;
            time = this.timeMotifEnd ? " " + this.timeMotifEnd : " 12:00";
            data.datetime_motif_end += time;
            time = this.timeAppel ? " " + this.timeAppel : " 12:00";
            data.datetime_appel += time;
            // if (this.timeMotifStart) data.datetime_motif_start += " " + this.timeMotifStart;
            // if (this.timeMotifEnd) data.datetime_motif_end += " " + this.timeMotifEnd;
            // if (this.timeAppel) data.datetime_appel += " " + this.timeAppel;

            // Set is_student.
            if (data.matricule_id) data.is_student = true;

            let modal = this;
            // Send data.
            let token = { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
            axios.post('/appels/api/appel/', data, token)
            .then(response => {
                this.hide();
                this.errors = {};
                this.$emit('update');
            }).catch(function (error) {
                modal.errors = error.response.data;
            });
        },
        getNameOptions(query) {
            this.searchId += 1;
            let currentSearch = this.searchId;
            this.nameLoading = true;
            axios.get("/annuaire/api/?query=" + query)
            .then(response => {
                // Avoid that a previous search overwrites a faster following search results.
                if (this.searchId !== currentSearch)
                    return;
                this.nameOptions = response.data.map(p => {
                    // Format entries.
                    let entry = {display: p.last_name + " " + p.first_name, matricule: p.matricule};
                    if ('classe' in p) {
                        // It's a student.
                        entry.display += " " + p.classe.year + p.classe.letter.toUpperCase();
                        entry.display += " – " + p.teaching.display_name;
                    } else {
                        // It's a responsible.
                        let teachings = " —";
                        for (let t in p.teaching) {
                            teachings += " " + p.teaching[t].display_name;
                        }
                        entry.display += teachings;
                    }
                    return entry;
                });
                this.nameLoading = false;
            })
            .catch(function (error) {
                this.nameLoading = false;
            });
        },
    },
    components: {Multiselect},
    mounted: function () {
        // Set motive options.
        axios.get('/dossier_eleve/api/info/')
        .then(response => {
            this.infoOptions = response.data.results.map(m => {
                return {value: m.id, text: m.info};
            });
        });
        // Set object options.
        axios.get('/dossier_eleve/api/sanction_decision/')
        .then(response => {
            this.sanctionDecisionOptions = response.data.results.map(m => {
                return {value: m.id, text: m.sanction_decision};
            });
        });
    }
}
</script>

<style>
</style>
