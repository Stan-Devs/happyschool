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
        :ok-disabled="!form.sanction_decision_id"
        ref="askModal"
        @ok="askSanction" @hidden="resetModal"
        >
        <b-row>
            <b-col sm="4">
                <div>
                    <b-img rounded :src="'/static/photos/' + name.matricule + '.jpg'" fluid alt="Photo de l'élève" />
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
                                    placeholder="Rechercher un étudiant…"
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
                        <b-form-group label="Demandeur" label-for="input-demandeur" :state="inputStates.demandeur">
                            <multiselect id="input-demandeur"
                                :internal-search="false"
                                :options="demandeurOptions"
                                @search-change="getDemandeurOptions"
                                :loading="demandeurLoading"
                                placeholder="Rechercher un responsable…"
                                select-label=""
                                selected-label="Sélectionné"
                                deselect-label=""
                                label="display"
                                track-by="display"
                                v-model="demandeur"
                                >
                                <span slot="noResult">Aucun responsable trouvée.</span>

                            </multiselect>
                            <span slot="invalid-feedback">{{ errorMsg('demandeur') }}</span>
                        </b-form-group>
                    </b-form-row>
                    <b-form-row>
                        <b-form-checkbox v-model="form.important">
                            Marquer comme important.
                        </b-form-checkbox>
                    </b-form-row>
                    <b-form-row class="mt-2">
                        <b-col sm="7">
                            <b-form-group label="Sanction et décision disciplinaire" label-for="input-info" :state="inputStates.sanction_decision_id">
                                <b-form-select id="input-info" v-model="form.sanction_decision_id" :options="sanctionOptions">
                                    <template slot="first">
                                        <option :value="null" disabled>Choisissez un type de sanction</option>
                                    </template>
                                </b-form-select>
                                <span slot="invalid-feedback">{{ errorMsg('sanction_decision_id') }}</span>
                            </b-form-group>
                            <b-form-group label="Date du conseil" label-for="input-date-conseil" :state="inputStates.datetime_conseil">
                                <b-form-input id="input-date-conseil" type="date" v-model="form.datetime_conseil"></b-form-input>
                                <span slot="invalid-feedback">{{ errorMsg('datetime_conseil') }}</span>
                            </b-form-group>
                            <b-form-group label="Date de la sanction" label-for="input-date-sanction" :state="inputStates.datetime_sanction">
                                <b-form-input id="input-date-sanction" type="date" v-model="form.datetime_sanction"></b-form-input>
                                <span slot="invalid-feedback">{{ errorMsg('datetime_sanction') }}</span>
                            </b-form-group>
                            <b-form-group label="Heure de la sanction" label-for="input-time-sanction">
                                <b-form-input id="input-time-sanction" type="time" v-model="timeSanction"></b-form-input>
                            </b-form-group>
                        </b-col>
                        <b-col sm="5">
                            <b-list-group>
                                <b-list-group-item class="d-flex justify-content-between align-items-center"
                                    v-for="(val, index) in stats" :key="index">
                                    <strong>{{ val.display }} :</strong> {{ val.value }}
                                </b-list-group-item>
                            </b-list-group>
                        </b-col>
                    </b-form-row>
                    <b-form-row>
                        <b-col>
                            <b-form-group label="Commentaires" label-for="input-comment" :state="inputStates.explication_commentaire">
                                <b-form-textarea id="input-comment" :rows="3" v-model="form.explication_commentaire"></b-form-textarea>
                                <span slot="invalid-feedback">{{ errorMsg('explication_commentaire') }}</span>
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
    props: ['entry'],
    data: function () {
        return {
            form: {
                name: "",
                matricule_id: null,
                sanction_decision_id: null,
                explication_commentaire: "",
                important: false,
                demandeur: "",
                datetime_sanction: null,
                datetime_conseil: null,
            },
            sanctionOptions: [],
            name: {matricule: null},
            nameOptions: [],
            nameLoading: false,
            demandeur: {},
            demandeurOptions: [],
            demandeurLoading: false,
            searchId: 0,
            stats: {},
            timeSanction: null,
            errors: {},
            inputStates: {
                name: null,
                sanction_decision_id: null,
                demandeur: null,
                explication_commentaire: null,
            },
        }
    },
    watch: {
        name: function () {
            // Update form data.
            if (this.name.matricule) {
                // First update form name data.
                this.form.name = this.name.display;
                this.form.matricule_id = this.name.matricule;
                // Get statistics.
                axios.get('dossier_eleve/api/statistics/' + this.name.matricule + '/')
                .then(response => {
                    this.stats = JSON.parse(response.data);
                })
                .catch(function (error) {
                    alert(error);
                });
            }
        },
        errors: function (newErrors, oldErrors) {
            let inputs = ['name', 'sanction_decision_id', 'demandeur', 'explication_commentaire',
            'datetime_conseil', 'datetime_sanctionl'];
            for (let u in inputs) {
                if (inputs[u] in newErrors) {
                    this.inputStates[inputs[u]] = newErrors[inputs[u]].length == 0;
                } else {
                    this.inputStates[inputs[u]] = null;
                }
            }
        },
        entry: function (entry, oldEntry) {
            if (entry) {
                // The name will update form.name and form.matricule_id
                this.name = {
                    display: entry.name,
                    matricule: entry.matricule_id,
                }
                this.demandeur = {
                    display: entry.demandeur,
                }
                this.form.explication_commentaire = entry.explication_commentaire;
                this.form.important = entry.important;

                this.form.sanction_decision_id = entry.sanction_decision_id;
                if (entry.datetime_sanction) {
                    let datetime = Moment(entry.datetime_sanction);
                    this.form.datetime_sanction = datetime.format('YYYY-MM-DD');
                    this.timeSanction = datetime.format('HH:MM');
                }
                if (entry.datetime_conseil) {
                    this.form.datetime_conseil = Moment(entry.datetime_conseil).format('YYYY-MM-DD');
                }
            } else {
                this.resetModal();
            }
        },
    },
    methods: {
        show: function () {
            this.$refs.askModal.show();
        },
        hide: function () {
            this.$refs.askModal.hide();
        },
        resetModal: function () {
            this.$emit('reset');

            this.name = {matricule: null};
            this.demandeur = {};
            this.stats = {};

            this.form.name = "";
            this.form.matricule_id = null;
            this.form.sanction_decision_id = null;
            this.form.explication_commentaire = "";
            this.form.important = false;
            this.form.demandeur = "";
            this.form.datetime_sanction = null;
            this.form.datetime_conseil = null;
        },
        errorMsg(err) {
            if (err in this.errors) {
                return this.errors[err][0];
            } else {
                return "";
            }
        },
        askSanction: function (evt) {
            evt.preventDefault();

            this.form.demandeur = this.demandeur.display;
            let data = this.form;
            // Add times if any.
            if (data.datetime_sanction) {
                let time = this.timeSanction ? " " + this.timeSanction : " 12:00";
                data.datetime_sanction += time;
            }
            if (data.datetime_conseil) {
                data.datetime_conseil += " 12:00";
            }

            let modal = this;
            // Send data.
            const token = { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};

            let path = '/dossier_eleve/api/ask_sanctions/'
            if (this.entry) path += this.entry.id + '/'
            const send = this.entry ? axios.put(path, data, token) : axios.post(path, data, token);
            send.then(response => {
                this.hide();
                this.errors = {};
                this.$emit('update');
            }).catch(function (error) {
                modal.errors = error.response.data;
            });
        },
        getNameOptions(query) {
            return this.getPeopleOptions(query, 'student');
        },
        getDemandeurOptions(query) {
            return this.getPeopleOptions(query, 'responsible');
        },
        getPeopleOptions(query, people) {
            let app = this;
            this.searchId += 1;
            let currentSearch = this.searchId;
            if (people == 'student') this.nameLoading = true;
            if (people == 'responsible') this.demandeurLoading = true;

            const token = { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
            const data = {
                query: query,
                teachings: this.$store.state.settings.teachings,
                people: people,
                check_access: true,
            };
            axios.post('/annuaire/api/people/', data, token)
            .then(response => {
                // Avoid that a previous search overwrites a faster following search results.
                if (this.searchId !== currentSearch)
                    return;
                const options = response.data.map(p => {
                    // Format entries.
                    let entry = {display: p.last_name + " " + p.first_name, matricule: p.matricule};
                    if ('is_secretary' in p) {
                        // It's a responsible.
                        let teachings = " —";
                        for (let t in p.teaching) {
                            teachings += " " + p.teaching[t].display_name;
                        }
                        entry.display += teachings;
                    } else {
                        // It's a student.
                        entry.display += " " + p.classe.year + p.classe.letter.toUpperCase();
                        entry.display += " – " + p.teaching.display_name;
                    }
                    return entry;
                });
                if (people == 'student') {
                    this.nameLoading = false;
                    this.nameOptions = options;
                } else if (people == 'responsible') {
                    this.demandeurLoading = false;
                    this.demandeurOptions = options;
                }
            })
            .catch(function (error) {
                alert(error);
                app.nameLoading = false;
            });
        },
    },
    mounted: function () {
        // Set sanctions and decisions options.
        axios.get('/dossier_eleve/api/sanction_decision/?only_sanctions=1')
        .then(response => {
            this.sanctionOptions = response.data.results.map(m => {
                return {value: m.id, text: m.sanction_decision};
            });
        })
        .catch(function (error) {
            alert(error);
        });
    },
    components: {Multiselect},
}
</script>

<style>
</style>
