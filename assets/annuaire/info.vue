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
            <b-card :title="lastName + ' ' + firstName" no-body>
                <b-tabs card>
                    <b-tab title="Info générale" active>
                        <b-row>
                            <b-col md="5" sm="12">
                                <div>
                                    <b-img rounded fluid :src="photoPath" fluid alt="Photo de l'élève" />
                                </div>
                            </b-col>
                            <b-col>
                                <dl class="row">
                                    <dt class="col-5 text-right">Nom </dt>
                                    <dd class="col-7">{{ lastName }}</dd>
                                    <dt class="col-5 text-right">Prénom </dt>
                                    <dd class="col-7">{{ firstName }}</dd>
                                    <dt class="col-5 text-right">Matricule</dt>
                                    <dd class="col-7">{{ matricule }}</dd>
                                    <dt v-if="tenure" class="col-5 text-right">Titulariat</dt>
                                    <dd v-if="tenure" v-for="(t, index) in tenure" :key="t.id"
                                        :class="{'col-7': index == 0, 'col-7 offset-5': index > 0}">
                                        {{ t.year }}{{ t.letter.toUpperCase()}}
                                    </dd>
                                    <dt class="col-5  text-right">Enseignement(s) </dt>
                                    <dd v-for="(t, index) in teachings" :key="t.id"
                                        :class="{'col-7': index == 0, 'col-7 offset-5': index > 0}">
                                        {{ t.display_name }}
                                    </dd>
                                    <dt class="col-5  text-right">Classe(s) </dt>
                                    <dd v-for="(c, index) in classe" :key="c.id"
                                        :class="{'col-7': index == 0, 'col-7 offset-5': index > 0}">
                                        {{ c.year }}{{ c.letter.toUpperCase()}}
                                    </dd>
                                    <dt v-if="type === 'student'" class="col-5 text-right">Date de naissance </dt>
                                    <dd v-if="type === 'student'" class="col-7">{{ niceDate(student_info.birth_date) }}</dd>
                                    <dt v-if="type === 'student'" class="col-5 text-right">Adresse </dt>
                                    <dd v-if="type === 'student'" class="col-7">{{ student_info.street }}</dd>
                                    <dd v-if="type === 'student'" class="col-7 offset-5">{{ student_info.postal_code }} – {{ student_info.locality }}</dd>
                                </dl>
                                <dl class="row">
                                    <dt class="col-5 text-right">Nom d'utilisateur </dt>
                                    <dd class="col-7">{{ student_info.username }}</dd>
                                    <dt class="col-5 text-right">Mot de passe </dt>
                                    <dd v-if="showPassword" class="col-7">{{ student_info.password }}</dd>
                                    <dd v-else class="col-7">
                                        <b-btn size="sm" variant="light" @click="showPassword = true">Montrer le mot de passe</b-btn>
                                    </dd>
                                </dl>

                            </b-col>
                        </b-row>
                        <b-row v-if="important.length > 0">
                            <b-col>
                                <b-card no-body class="mb-1">
                                    <b-card-header header-tag="header" class="p-1">
                                        <b-btn block href="#" v-b-toggle.infos-importantes variant="danger">Infos importantes</b-btn>
                                    </b-card-header>
                                    <b-collapse id="infos-importantes">
                                        <b-card-body>
                                            <b-row>
                                                <b-col cols="3"><strong>Date</strong></b-col>
                                                <b-col cols="2"><strong>Objet/Motif</strong></b-col>
                                                <b-col><strong>Message</strong></b-col>
                                            </b-row>
                                            <b-row v-for="cas in important" :key="cas.id" class="mb-2">
                                                <b-col cols="3">{{ niceDate(cas.datetime_encodage) }}</b-col>
                                                <b-col cols="2">{{ cas.sanction_decision ? cas.sanction_decision.sanction_decision : cas.info.info }}</b-col>
                                                <b-col>{{ cas.explication_commentaire }}</b-col>
                                            </b-row>
                                        </b-card-body>
                                    </b-collapse>
                                </b-card>
                            </b-col>
                        </b-row>
                    </b-tab>
                    <b-tab title="Moyens de contacts" v-if="contact">
                        <dl class="row">
                            <dt class="col-5 text-right">Nom du responsable</dt>
                            <dd class="col-7">{{ contact.resp_last_name }} {{ contact.resp_first_name }}</dd>
                            <dt class="col-5 text-right">Téléphone responsable</dt>
                            <dd class="col-7">{{ contact.resp_phone }}</dd>
                            <dt class="col-5 text-right">GSM responsable</dt>
                            <dd class="col-7">{{ contact.resp_mobile }}</dd>
                            <dt class="col-5 text-right">Email responsable</dt>
                            <dd class="col-7"><a :href="'mailto:' + contact.resp_email">{{ contact.resp_email }}</a></dd>
                            <dt class="col-5 text-right">Nom de la mère</dt>
                            <dd class="col-7">{{ contact.mother_last_name }} {{ contact.mother_first_name }}</dd>
                            <dt class="col-5 text-right">Téléphone de la mère</dt>
                            <dd class="col-7">{{ contact.mother_phone }}</dd>
                            <dt class="col-5 text-right">GSM de la mère</dt>
                            <dd class="col-7">{{ contact.mother_mobile }}</dd>
                            <dt class="col-5 text-right">Email de la mère</dt>
                            <dd class="col-7"><a :href="'mailto:' + contact.mother_email">{{ contact.mother_email }}</a></dd>
                            <dt class="col-5 text-right">Nom du père</dt>
                            <dd class="col-7">{{ contact.father_last_name }} {{ contact.father_first_name }}</dd>
                            <dt class="col-5 text-right">Téléphone du père</dt>
                            <dd class="col-7">{{ contact.father_phone }}</dd>
                            <dt class="col-5 text-right">GSM du père</dt>
                            <dd class="col-7">{{ contact.father_mobile }}</dd>
                            <dt class="col-5 text-right">Email du père</dt>
                            <dd class="col-7"><a :href="'mailto:' + contact.father_email">{{ contact.father_email }}</a></dd>
                        </dl>
                    </b-tab>
                    <b-tab title="Info médicales" v-if="medical">
                        <dl class="row">
                            <dt class="col-5 text-right">Médecin</dt>
                            <dd class="col-7">{{ medical.doctor }}</dd>
                            <dt class="col-5 text-right">Téléphone médecin</dt>
                            <dd class="col-7">{{ medical.doctor_phone }}</dd>
                            <dt class="col-5 text-right">Mutuelle</dt>
                            <dd class="col-7">{{ medical.mutual }}</dd>
                            <dt class="col-5 text-right">Numéro mutuelle</dt>
                            <dd class="col-7">{{ medical.mutual_number }}</dd>
                            <dt class="col-5 text-right">Infos complémentaires</dt>
                            <dd class="col-7">{{ medical.medical_information }}</dd>
                        </dl>
                    </b-tab>
                </b-tabs>
            </b-card>
            <b-card v-if="last_news && dossier_eleve.length > 0" header="Derniers messages du dossier des élèves" class="mt-2">
                <b-row>
                    <b-col cols="2"><strong>Date</strong></b-col>
                    <b-col cols="2"><strong>Objet/Motif</strong></b-col>
                    <b-col><strong>Message</strong></b-col>
                </b-row>
                <b-row v-for="cas in dossier_eleve" :key="cas.id" class="mb-2">
                    <b-col cols="2" :class="cas.important ? ' important' : ''">{{ niceDate(cas.datetime_encodage) }}</b-col>
                    <b-col cols="2" :class="cas.important ? ' important' : ''">{{ cas.sanction_decision ? cas.sanction_decision.sanction_decision : cas.info.info }}</b-col>
                    <b-col :class="cas.important ? ' important' : ''">{{ cas.explication_commentaire }}</b-col>
                </b-row>
            </b-card>
            <b-card v-if="last_news && infirmerie.length > 0" header="Derniers passages à l'infirmerie" class="mt-2">
                <b-row>
                    <b-col cols="2"><strong>Arrivé</strong></b-col>
                    <b-col cols="2"><strong>Sortie</strong></b-col>
                    <b-col cols="2"><strong>Motifs d'admission</strong></b-col>
                    <b-col><strong>Remarques de sortie</strong></b-col>
                </b-row>
                <b-row v-for="passage in infirmerie" :key="passage.id" class="mb-2">
                    <b-col cols="2">{{ niceDate(passage.datetime_arrive) }}</b-col>
                    <b-col cols="2">{{ passage.datetime_sortie ? niceDate(passage.datetime_sortie) : '' }}</b-col>
                    <b-col cols="2">{{ passage.motifs_admission }}</b-col>
                    <b-col>{{ passage.remarques_sortie }}</b-col>
                </b-row>
            </b-card>
            <b-card v-if="last_news && appels.length > 0" header="Derniers appels" class="mt-2">
                <b-row>
                    <b-col cols="2"><strong>Date</strong></b-col>
                    <b-col cols="2"><strong>Objet</strong></b-col>
                    <b-col cols="2"><strong>Motif</strong></b-col>
                    <b-col><strong>Message</strong></b-col>
                </b-row>
                <b-row v-for="appel in appels" :key="appel.id" class="mb-2">
                    <b-col cols="2">{{ niceDate(appel.datetime_appel) }}</b-col>
                    <b-col cols="2">{{ appel.object.display }}</b-col>
                    <b-col cols="2">{{ appel.motive.display }}</b-col>
                    <b-col>{{ appel.commentaire }}</b-col>
                </b-row>
            </b-card>
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

import Moment from 'moment';
Moment.locale('fr');

export default {
    props: {
        matricule: Number,
        type: String,
        last_news: {
            type: Boolean,
            default: false,
        }
    },
    data: function () {
        return {
            lastName: '',
            firstName: '',
            showPassword: false,
            classe: [],
            tenure: null,
            teachings: [],
            student_info: {},
            contact: null,
            medical: null,
            important: [],
            dossier_eleve: [],
            appels: [],
            infirmerie: [],
        }
    },
    computed: {
        photoPath: function () {
            let path = '/static/photos'
            if (this.type == 'responsible') path += '_prof';
            return path + '/' + this.matricule + '.jpg'
        }
    },
    watch: {
        matricule: function () {
            this.loadInfo();
        }
    },
    methods: {
        reset: function () {
            this.student_info = {};
            this.contact = null;
            this.medical = null;
            this.showPassword = false;
            this.tenure = null;
            this.important = [];
            this.dossier_eleve = [];
            this.appels = [];
            this.infirmerie = [];
        },
        niceDate: function (date) {
            return Moment(date).calendar();
        },
        loadInfo: function () {
            this.reset();

            if (this.type == 'student') {
                axios.get('/annuaire/api/student/' + this.matricule + '/')
                .then(response => {
                    this.lastName = response.data.last_name;
                    this.firstName = response.data.first_name;
                    this.classe = [response.data.classe];
                    this.teachings = [response.data.teaching];
                });

                axios.get('/annuaire/api/info_general/' + this.matricule + '/')
                .then(response => {
                    this.student_info = response.data;
                });

                axios.get('/annuaire/api/info_contact/' + this.matricule + '/')
                .then(response => {
                    this.contact = response.data;
                });

                axios.get('/annuaire/api/info_medical/' + this.matricule + '/')
                .then(response => {
                    this.medical = response.data;
                });

                axios.get('/dossier_eleve/api/cas_eleve/?ordering=-datetime_encodage&important=true&matricule_id=' + this.matricule)
                .then(response => {
                    this.important = response.data.results;
                });

                if (this.last_news) {
                    axios.get('/dossier_eleve/api/cas_eleve/?ordering=-datetime_encodage&matricule_id=' + this.matricule)
                    .then(response => {
                        this.dossier_eleve = response.data.results.slice(0, 5);
                    });

                    axios.get('/appels/api/appel/?ordering=-datetime_appel&matricule_id=' + this.matricule)
                    .then(response => {
                        this.appels = response.data.results.slice(0, 5);
                    });

                    axios.get('/infirmerie/api/passage/?ordering=-datetime_passage&matricule_id=' + this.matricule)
                    .then(response => {
                        this.infirmerie = response.data.results.slice(0, 5);
                    });
                }
            } else if (this.type == 'responsible') {
                axios.get('/annuaire/api/responsible/' + this.matricule + '/')
                .then(response => {
                    this.lastName = response.data.last_name;
                    this.firstName = response.data.first_name;
                    this.classe = response.data.classe;
                    this.teachings = response.data.teaching;
                    this.tenure = response.data.tenure;
                })
            }
        }
    },
    mounted: function () {
        this.loadInfo();
    }
}
</script>

<style>
.important {
    background-color: rgba(255, 0, 0, 0.3);
}
</style>
