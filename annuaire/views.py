# This file is part of HappySchool.
#
# HappySchool is the legal property of its developers, whose names
# can be found in the AUTHORS file distributed with this source
# distribution.
#
# HappySchool is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# HappySchool is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with HappySchool.  If not, see <http://www.gnu.org/licenses/>.

from django.conf import settings
from django.shortcuts import render

from django.http import Http404, JsonResponse, HttpResponse
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from rest_framework.views import APIView, Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from z3c.rml import rml2pdf
from unidecode import unidecode

from core.people import People, get_classes
from core.models import StudentModel, ClasseModel, TeachingModel, ResponsibleModel, AdditionalStudentInfo
from core.serializers import StudentSerializer, ResponsibleSensitiveSerializer, ClasseSerializer,\
    StudentGeneralInfoSerializer, StudentContactInfoSerializer, StudentMedicalInfoSerializer

from .models import AnnuaireSettingsModel
from .serializers import AnnuaireSettingsSerializer

# from core.Person import Person
# from core.Student import Student
#
# from core.StudentManager import StudentManager
# from core.TeacherManager import TeacherManager
# from core.EducatorManager import EducatorManager
# from core.models import StudentLDAP
# from core.utility import get_new_rows
#
# from auth_libreschool.views import get_classes_access


from .forms import ChercherEleveForm

# student_man = StudentManager()
# teacher_man = TeacherManager()
# educator_man = EducatorManager()

groups_with_access = [settings.SYSADMIN_GROUP, settings.TEACHER_GROUP, settings.DIRECTION_GROUP, settings.EDUCATOR_GROUP,
                      settings.SECRETARY_GROUP, settings.RECEPTION_GROUP, settings.PMS_GROUP]

@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=groups_with_access), login_url='no_access')
def get_list(request):
    # Récuparation des variables GET

    ens = request.GET.get("ens", "all").lower()
    search = request.GET.get("search", "")
    matricule = request.GET.get("mat", "")
    classe = request.GET.get("classe", "")
    people_type = request.GET.get("type", "student")

    if people_type == 'teacher' and request.user.groups.filter(name__in=[settings.SYSADMIN_GROUP, settings.DIRECTION_GROUP, settings.RECEPTION_GROUP]).exists():
        return get_teacher_list(request, ens, search)

    students = []
    if matricule:
        students = [People().get_student_by_id(int(matricule), [ens])]
        # students = [student_man.get_person(int(matricule))]
    elif classe:
        an = classe[0]
        classe_letter = classe[1]
        classe = ClasseModel.objects.get(year=int(an), letter=classe_letter.lower(), teaching__name=ens)
        students = StudentModel.objects.filter(classe=classe)
    else:
        if search.isdigit() and len(search) == 4:
            # We are looking for a matricule
            students = People().get_student_by_id(int(matricule))
        elif search[0].isdigit() :
            # We are looking for a class
            classes = ClasseModel.objects.filter(year=int(search[0]))
            if ens != "all":
                classes = classes.filter(teaching__name=ens)
            if len(search) > 1:
                classes = classes.filter(letter=search[1])

            students = StudentModel.objects.filters(classe=classes)
        else:
            students = People().get_students_by_name(search, [ens])
            # students = student_man.get_people_by_names(ens, search)

    context = {}
    if classe:
        context['classe'] = classe.letter
        context['year'] = classe.year
        context['enseignement'] = ens
        students = sorted(students, key=lambda s: unidecode(s.last_name.lower()))

    context['eleves'] = students
    return render(request, 'annuaire/list.html', context=context)


def get_teacher_list(request, ens, search):
    teachers = []
    if search != "":
        # teachers = teacher_man.get_people_by_names(ens, search)
        teachers = People().get_teachers_by_name(search, [ens])

    return render(request, 'annuaire/list_teacher.html', {'teachers': teachers})


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=groups_with_access),
                  login_url='no_access')
def index(request):
    chercher_form = ChercherEleveForm()

    # Set a long time expiracy for accuiel
    if request.user.username == 'accueil':
        request.session.set_expiry(100000000)

    #TODO: context = {'form': chercher_form, 'new_rows': get_new_rows(request)}
    context = {'form': chercher_form, 'new_rows': 0}
    if request.user.groups.filter(name__in=[settings.SYSADMIN_GROUP, settings.DIRECTION_GROUP, settings.RECEPTION_GROUP]).exists():
        context['can_search_teachers'] = True
    return render(request, 'annuaire/index.html', context)


@login_required
def info(request, matricule, medical_info='1', user_info='1'):
    try:
        # student = student_man.get_person(matricule)
        student = People().get_student_by_id(matricule)
    except StopIteration:
        raise Http404("Matricule inexistant : " + str(matricule))

    context = {'student': student, 'medical_info': medical_info, 'user_info': user_info }

    return render(request, 'annuaire/eleve_info.html', context=context)


@login_required
def info_teacher(request, matricule):
    if not request.user.groups.filter(name__in=[settings.SYSADMIN_GROUP, settings.DIRECTION_GROUP, settings.RECEPTION_GROUP]).exists():
        raise Http404("ID inexistant : " + str(id))


    # teacher = teacher_man.get_person(matricule, ens)
    teacher = People().get_teacher_by_id(matricule)
    if not teacher:
        raise Http404("Matricule inexistant : " + str(matricule))
    context = {'teacher': teacher}
    if request.user.groups.filter(name__in=[settings.SYSADMIN_GROUP, settings.DIRECTION_GROUP]).exists():
        context['username_info'] = True

    return render(request, 'annuaire/professeur_info.html', context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=groups_with_access),
                  login_url='no_access')
def summary(request, matricule):
    # eleve = student_man.get_person(matricule)
    eleve = People().get_student_by_id(matricule)
    if not eleve:
        raise Http404("Matricule inexistant : " + str(matricule))

    context = {'eleve': eleve.__dict__}
    #TODO: infirmerie, appels, dossier_eleve
    if 'infirmerie' in settings.INSTALLED_APPS:
        from infirmerie.views import filter_and_order
        context['infirmerie'] = filter_and_order(request,
                                             column="matricule",
                                             data1=eleve.matricule,
                                             order_by="datetime_encodage",
                                             order_asc="desc")[:5]

    if 'appels' in settings.INSTALLED_APPS:
        from appels.views import filter_and_order
        context['appels'] = filter_and_order(request,
                                             column="matricule",
                                             data1=eleve.matricule,
                                             order_by="datetime_encodage",
                                             order_asc="desc")[:5]

    if 'dossier_eleve' in settings.INSTALLED_APPS:
        from dossier_eleve.views import filter_and_order
        context['dossier_eleve'] = filter_and_order(request,
                                                    column="matricule",
                                                    data1=eleve.matricule,
                                                    order_by="datetime_encodage",
                                                    order_asc="desc")[:5]

    return render(request, 'annuaire/eleve.html', context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=[settings.SYSADMIN_GROUP, settings.DIRECTION_GROUP, settings.RECEPTION_GROUP]),
                  login_url='no_access')
def summary_teacher(request, id):
    if not request.user.groups.filter(name__in=[settings.SYSADMIN_GROUP, settings.DIRECTION_GROUP, settings.RECEPTION_GROUP]).exists():
        raise Http404("ID inexistant : " + str(id))

    # teacher = teacher_man.get_person(id, ens)
    teacher = People().get_teacher_by_id(id)
    if not teacher:
        raise Http404("ID inexistant : " + str(id))

    context = {'teacher': teacher}
    return render(request, 'annuaire/professeur.html', context)


@login_required
def get_students_names(request, enseignement="all"):
    return get_people_names(request, enseignement, 'student')


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=groups_with_access),
                  login_url='no_access')
def get_students_matricules(request):
    suggestions = []
    filter_str = request.GET.get('query', '')
    if filter_str == '':
        return JsonResponse([], safe=False)

    #TODO students matricule
    # eleves = student_man.get_people(filters=['matricule=' + filter_str + '*'])
    #
    #
    # for e in eleves:
    #     cn = e.surname
    #     sn = e.firstname
    #     matricule = str(e.matricule)
    #     if not matricule.startswith(filter_str):
    #         continue
    #
    #     classe = e.classe
    #     suggestions.append({'id': cn + ' ' + sn + ' ' + classe, 'name': e.matricule})

    return JsonResponse(suggestions, safe=False)


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=groups_with_access),
                  login_url='no_access')
def get_students_or_classes(request, enseignement='all', check_access="0"):
    query = request.GET.get('query', '')
    enseignement = request.GET.get("ens", enseignement)
    check_access = check_access == "1"
    if query[0].isdigit():
        if len(query) > 1:
            classes_list = create_classes_list(request, enseignement, check_access=check_access,
                                               annees=query[0], letters=query[1])
        else:
            classes_list = create_classes_list(request, enseignement, check_access=check_access, annees=(query[0]))
        return format_classes_to_json(classes_list)
    else:
        return get_people_names(request, enseignement, people_type='student', check_access=check_access)


def create_classes_list(request, enseignement="all", check_access=False, annees="", letters=""):
    classes = get_classes([enseignement], check_access, request.user)

    if annees:
        classes = classes.filter(year=annees)

    if letters:
        classes = classes.filter(letter=letters.lower())

    return list(map(lambda c: str(c), classes))


def format_classes_to_json(classes):
    suggestions = list(map(lambda c: {'id': c.replace(" – ", "-"), 'name': c}, classes))
    return JsonResponse(suggestions, safe=False)


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=groups_with_access),
                  login_url='no_access')
def get_people_names(request, enseignement='all', people_type='all', formatting='json', check_access=False):
    people = []
    query = request.GET.get('query', '')

    if people_type == 'responsible' or people_type == 'all':
        people += People().get_responsibles_by_name(query, [enseignement])

    if people_type == 'teacher':
        people += People().get_teachers_by_name(query, [enseignement])

    if people_type == 'educator':
        people += People().get_educators_by_name(query, [enseignement])

    if people_type == 'student' or people_type == 'all':
        classe_years = get_classes([enseignement], check_access=True, user=request.user) if check_access else None
        people += People().get_students_by_name(query, [enseignement], classes=classe_years)

    if formatting == 'json':
        return format_name_to_json(people, people_type)

    return people


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=groups_with_access),
                  login_url='no_access')
def get_teachers_emails(request, enseignement='secondaire'):
    query = request.GET.get('query', '')
    if query == '':
        return JsonResponse([], safe=False)

    teachers = People().get_teachers_by_name(query, [enseignement])
    # teachers = teacher_man.get_people_by_names(enseignement, search_string=query)
    teachers = list(map(lambda t: t.gen_email, teachers))
    return JsonResponse(teachers, safe=False)


def format_name_to_json(people_list, people_type):
    suggestions = []
    for p in people_list:
        display_name = p.fullname
        if type(p) == StudentModel:
            display_name += ' ' + p.classe.compact_str
            if p.teaching.name == 'primaire':
                display_name += ' ' + 'Prim.'

        suggestions.append({'name': display_name, 'id': p.matricule})

    return JsonResponse(suggestions, safe=False)


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=groups_with_access),
                  login_url='no_access')
def get_class_photo_pdf(request, year, classe, enseignement):
    students = StudentModel.objects.filter(classe__year=year, classe__letter=classe, classe__teaching__name=enseignement)

    students = sorted(students, key=lambda s: unidecode(s.last_name.lower()))
    rows = []
    student_by_row = 6
    row = []
    for i, student in enumerate(students):
        if i % student_by_row == 0:
            row = []
        row.append(student)
        if i % student_by_row == student_by_row - 1 or len(students) == i + 1:
            rows.append(row)

    context = {'classe': str(year) + classe , 'list': rows, 'students_numb': len(students)}

    # teaching = TeachingModel.objects.get(name=enseignement)
    classe = ClasseModel.objects.get(year=year, letter=classe, teaching__name=enseignement)
    tenures = ResponsibleModel.objects.filter(tenure=classe)
    # tenures = teacher_man.get_people(enseignement=enseignement,
                                    # filters=['tenure=%s%s' % (year, classe)])
    context['tenures'] = tenures

    context['absolute_path'] = settings.BASE_DIR
    t = get_template('annuaire/classe.rml')
    rml_str = t.render(context)

    pdf = rml2pdf.parseString(rml_str)
    if not pdf:
        return render(request, 'dossier_eleve/no_student.html')
    pdf_name = 'classes_%s%s.pdf' % (year, classe)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename; filename="' + pdf_name + '"'
    response.write(pdf.read())
    return response


def get_settings():
    settings_annuaire = AnnuaireSettingsModel.objects.first()
    if not settings_annuaire:
        # Create default settings.
        AnnuaireSettingsModel.objects.create().save()

    return settings_annuaire


class AnnuaireView(LoginRequiredMixin,
                       TemplateView):
    template_name = "annuaire/annuaire.html"

    def get_context_data(self, **kwargs):
        # Add to the current context.
        context = super().get_context_data(**kwargs)
        context['settings'] = JSONRenderer().render(AnnuaireSettingsSerializer(get_settings()).data).decode()
        return context


def search_classes(query, teachings, check_access, user):
    if len(query) == 0:
        return []

    if not query[0].isdigit():
        return []

    truncate = True
    classes = get_classes(teaching=teachings, check_access=check_access, user=user)
    classes = classes.filter(year=query[0]).order_by('year', 'letter')
    if len(query) > 1:
        classes = classes.filter(letter=query[1].lower())

    if truncate:
        classes = classes[:100]

    return ClasseSerializer(classes, many=True).data


def search_people(query, people_type, teachings, check_access, user):
    def serialize_people(person):
        if type(person) == StudentModel:
            return StudentSerializer(person).data
        elif type(person) == ResponsibleModel:
            return ResponsibleSensitiveSerializer(person).data

    if len(query) < 1:
        return []

    truncate_limit = 50
    people = []
    if people_type == 'responsible' or people_type == 'all':
        people += ResponsibleSensitiveSerializer(
            People().get_responsibles_by_name(query, teachings)[:truncate_limit], many=True
        ).data

    if people_type == 'teacher':
        people += ResponsibleSensitiveSerializer(
            People().get_teachers_by_name(query, teachings)[:truncate_limit], many=True
        ).data

    if people_type == 'educator':
        people += ResponsibleSensitiveSerializer(
            People().get_educators_by_name(query, teachings)[:truncate_limit], many=True
        ).data

    if people_type == 'student' or people_type == 'all':
        classe_years = get_classes(teachings, check_access=True,
                                   user=user) if check_access else None
        people += StudentSerializer(
            People().get_students_by_name(query, teachings, classes=classe_years)[:truncate_limit], many=True
        ).data

    return people[:truncate_limit]


class SearchPeopleAPI(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)

    def get(self, request, format=None):
        query = request.GET.get('query', '')
        people_type = request.GET.get('people', 'all')
        teachings = request.GET.get('teaching', 'all')
        check_access = request.GET.get('check_access', '0') == 1

        people = search_people(query=query, people_type=people_type, teachings=teachings,
                               check_access=check_access, user=request.user)
        return Response(people)

    def post(self, request, format=None):
        query = request.data.get('query', '')
        people_type = request.data.get('people', 'all')
        teachings = TeachingModel.objects.filter(id__in=request.data.get('teachings', []))
        check_access = request.data.get('check_access', 0) == 1

        people = search_people(query=query, people_type=people_type, teachings=teachings,
                               check_access=check_access, user=request.user)
        return Response(people)


class SearchClassesAPI(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        query = request.data.get('query', '')
        teachings = TeachingModel.objects.filter(id__in=request.data.get('teachings', []))
        check_access = request.data.get('check_access', 0) == 1

        classes = search_classes(query=query, teachings=teachings,
                                 check_access=check_access, user=request.user)
        return Response(classes)


class SearchClassesOrPeopleAPI(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        query = request.data.get('query', '')
        people_type = request.data.get('people', 'student')
        teachings = TeachingModel.objects.filter(id__in=request.data.get('teachings', []))
        check_access = request.data.get('check_access', 0) == 1

        if len(query) == 0:
            return Response([])

        if query[0].isdigit():
            return Response(search_classes(query=query, teachings=teachings,
                                           check_access=check_access, user=request.user))

        people = search_people(query=query, people_type=people_type, teachings=teachings,
                               check_access=check_access, user=request.user)
        return Response(people)


class StudentClasseAPI(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)

    def get(self, request, format=None):
        classe_id = request.GET.get('classe', None)
        print(classe_id)
        if not classe_id or not classe_id.isdigit:
            return Response([])

        students = StudentModel.objects.filter(classe__id=classe_id).order_by('last_name', 'first_name')
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)


class StudentInfoViewSet(ReadOnlyModelViewSet):
    queryset = StudentModel.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (IsAuthenticated,)


class ResponsibleInfoViewSet(ReadOnlyModelViewSet):
    queryset = ResponsibleModel.objects.all()
    serializer_class = ResponsibleSensitiveSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "matricule"


class StudentGeneralInfoViewSet(ReadOnlyModelViewSet):
    queryset = AdditionalStudentInfo.objects.all()
    serializer_class = StudentGeneralInfoSerializer
    permission_classes = (IsAuthenticated,)


class StudentContactInfoViewSet(ReadOnlyModelViewSet):
    queryset = AdditionalStudentInfo.objects.all()
    serializer_class = StudentContactInfoSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        allowed_groups = get_settings().can_see_student_contact.all()
        if not self.request.user.groups.intersection(allowed_groups).exists():
            return AdditionalStudentInfo.objects.none()

        return super().get_queryset()


class StudentMedicalInfoViewSet(ReadOnlyModelViewSet):
    queryset = AdditionalStudentInfo.objects.all()
    serializer_class = StudentMedicalInfoSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        allowed_groups = get_settings().can_see_student_medical.all()
        if not self.request.user.groups.intersection(allowed_groups).exists():
            return AdditionalStudentInfo.objects.none()

        return super().get_queryset()
