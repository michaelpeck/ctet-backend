import pandas as pd
from datetime import datetime
from django.conf import settings

from clinical_effort.models import CTEffort, TrialArms, PersonnelTypes
from ..serializers import CTEffortSerializer

from .sections.general import get_general_df
from .sections.complexity import get_complexity_df
from .sections.personnel import get_person_arm_df
from .sections.structure import get_structure_df
from .sections.time_allocations import get_summary_df, edit_summary_df, get_subject_summary_df, get_total_summary_df, get_person_arm_hours_df, edit_person_arm_hours_df
from .sections.summary import get_summary_fte_df, get_person_arm_fte_df


# Create new project
def create_export(id):

    # Get objects
    people = CTEffort.objects.filter(id=id)[0].personnel_set.all()
    arms = CTEffort.objects.filter(id=id)[0].trialarms_set.all()

    # Create file
    now = datetime.now()
    filepath = settings.MEDIA_ROOT + 'exports/ctet_' + id + '_export_' + now.strftime("%m%d%Y") + '_' + now.strftime("%H%M%S") + '.xlsx'

    # Create sheet
    with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:

        # Formatting
        workbook  = writer.book

        # Add a header format.
        header_format = workbook.add_format({
            'bold': True,
            'align': 'left',
            'font_size': 18})

        body_format = workbook.add_format({
            'bold': False,
            'align': 'left',
            'font_size': 18})

        # Project
        df_gen = get_general_df(proj_id = id)
        df_gen.to_excel(writer, sheet_name='general', index=False, header=False)

        # Project format
        worksheet_gen = writer.sheets['general']
        # Write the column headers with the defined format.
        worksheet_gen.set_column(0, 0, 36, header_format)
        worksheet_gen.set_column(1, 1, 48, body_format)

        # Personnel
        df_personnel = pd.DataFrame.from_records(CTEffort.objects.filter(id=id)[0].personnel_set.values('name', 'type', 'year_hours', 'addl_lump_hours', 'updated'))
        df_personnel['updated'] = df_personnel['updated'].dt.tz_localize(None)
        df_personnel['updated'] = df_personnel['updated'].dt.strftime("%m/%d/%Y")
        df_personnel.to_excel(writer, sheet_name='personnel', index=False)
        # Personnel formatting
        worksheet_personnel = writer.sheets['personnel']
        personnel_titles = ['Name', 'Type', 'Hours/Year', 'Additional Lump Sum Hours', 'Updated at']
        for col_num, value in enumerate(df_personnel.columns.values):
            worksheet_personnel.set_column(col_num, col_num, 36, body_format)
            worksheet_personnel.write(0, col_num, personnel_titles[col_num], header_format)
        for index, row in df_personnel.iterrows():
            type = PersonnelTypes.objects.get(id=row['type']).name
            worksheet_personnel.write(index + 1, 1, type, body_format)

        # Structure
        structure_titles = ['Cycle Name', '# Cycles', '# Visits', 'Copy Effort?']
        structure_widths = [36, 20, 20, 20]
        row_index = 0

        for arm in arms:
            # Add arm name row
            arm_name = pd.DataFrame(columns=[arm.name])
            arm_name.to_excel(writer, sheet_name='structure', index=False, startrow=row_index)
            worksheet_structure = writer.sheets['structure']
            worksheet_structure.write(row_index, 0, arm_name.columns.values[0], header_format)
            row_index += 1
            # Get and add arm cycle df
            structure_df = get_structure_df(id, arm)
            structure_df.to_excel(writer, sheet_name='structure', index=False, startrow=row_index)
            # Format
            for col_num, value in enumerate(structure_df.columns.values):
                worksheet_structure.set_column(col_num, col_num, structure_widths[col_num], body_format)
                worksheet_structure.write(row_index, col_num, structure_titles[col_num], header_format)
            row_index += structure_df.shape[0] + 2

        # Time Allocations
        row_index = 0
        summary_df = get_summary_df(id)
        person_arm_hours_df = get_person_arm_hours_df(id)
        for person in people:
            person_name = pd.DataFrame(columns=[person.name])
            person_name.to_excel(writer, sheet_name='time_allocations', index=False, startrow=row_index)
            worksheet_time = writer.sheets['time_allocations']
            worksheet_time.write(row_index, 0, person_name.columns.values[0], header_format)
            row_index += 1
            for arm in arms:
                # Arm names
                arm_name = pd.DataFrame(columns=[arm.name])
                arm_name.to_excel(writer, sheet_name='time_allocations', index=False, startrow=row_index)
                worksheet_time.write(row_index, 0, arm_name.columns.values[0], header_format)
                row_index += 1
                # Cycles & Visits
                cycles = arm.cycles_set.all()
                cycle_cols = ['Cycle (#)']
                visit_cols = ['Visit #']
                for cycle in cycles:
                    i = 1
                    visits = cycle.visits_set.all()
                    j = 0
                    for visit in visits:
                        j += 1
                        cycle_cols.append(cycle.name + ' (' + str(i) + ')')
                        visit_cols.append(str(j))
                    i += 1
                # Cycles
                cycles_df = pd.DataFrame(columns=cycle_cols)
                cycles_df.to_excel(writer, sheet_name='time_allocations', index=False, startrow=row_index)
                for col_num, value in enumerate(cycles_df.columns.values):
                    worksheet_time.write(row_index, col_num, value, header_format)
                row_index += 1
                # Visits
                visits_df = pd.DataFrame(columns=visit_cols)
                visits_df.to_excel(writer, sheet_name='time_allocations', index=False, startrow=row_index)
                for col_num, value in enumerate(visits_df.columns.values):
                    worksheet_time.write(row_index, col_num, value, header_format)
                row_index += 1
                # Person arm df
                p_a_df = get_person_arm_df(id, person.id, arm.id)
                p_a_df.to_excel(writer, sheet_name='time_allocations', index=False, startrow=row_index)
                # Format
                for col_num, value in enumerate(p_a_df.columns.values):
                    if col_num == 0:
                        width = 36
                    else:
                        width = 16
                    worksheet_time.set_column(col_num, col_num, width, body_format)
                    worksheet_time.write(row_index, col_num, value, header_format)
                row_index += p_a_df.shape[0] + 2
                summary_df = edit_summary_df(summary_df, p_a_df.loc['sum'], person)
                person_arm_hours_df = edit_person_arm_hours_df(person_arm_hours_df, p_a_df.loc['sum'], person, arm)

        # Person arm hours table
        # person_arm_hours_df.to_excel(writer, sheet_name='time_allocations', index=False, startrow=row_index)
        # for col_num, value in enumerate(person_arm_hours_df.columns.values):
        #     worksheet_time.write(row_index, col_num, value, header_format)
        # row_index += person_arm_hours_df.shape[0] + 2

        # Summary table
        summary_name = pd.DataFrame(columns=['Allocation Summary'])
        summary_name.to_excel(writer, sheet_name='time_allocations', index=False, startrow=row_index)
        worksheet_time.write(row_index, 0, summary_name.columns.values[0], header_format)
        row_index += 1
        # Add arm and cycle headers
        arm_cols = ['Arm']
        cycle_cols = ['Cycle (#)-(Visit #)']
        for arm in arms:
            cycles = arm.cycles_set.all()
            for cycle in cycles:
                i = 1
                visits = cycle.visits_set.all()
                j = 0
                for visit in visits:
                    j += 1
                    arm_cols.append(arm.name)
                    cycle_cols.append(cycle.name + ' (' + str(i) + ')-(' + str(j) + ')')
                i += 1

        # Arms
        arms_df = pd.DataFrame(columns=arm_cols)
        arms_df.to_excel(writer, sheet_name='time_allocations', index=False, startrow=row_index)
        for col_num, value in enumerate(arms_df.columns.values):
            worksheet_time.write(row_index, col_num, value, header_format)
        row_index += 1
        # Cycles
        cycles_df = pd.DataFrame(columns=cycle_cols)
        cycles_df.to_excel(writer, sheet_name='time_allocations', index=False, startrow=row_index)
        for col_num, value in enumerate(cycles_df.columns.values):
            worksheet_time.write(row_index, col_num, value, header_format)
        row_index += 1
        # Summary table
        summary_df.to_excel(writer, sheet_name='time_allocations', index=False, startrow=row_index)
        summary_titles = ['']
        for col_num, value in enumerate(summary_df.columns.values):
            if col_num == 0:
                width = 36
            else:
                width = 16
            worksheet_time.set_column(col_num, col_num, width, body_format)
            worksheet_time.write(row_index, col_num, value, header_format)
        row_index += summary_df.shape[0] + 2

        # Subject summary
        summary_name = pd.DataFrame(columns=['Per Subject Values'])
        summary_name.to_excel(writer, sheet_name='time_allocations', index=False, startrow=row_index)
        worksheet_time.write(row_index, 0, summary_name.columns.values[0], header_format)
        row_index += 1
        subject_summary_df = get_subject_summary_df(summary_df, people, arms)
        subject_summary_df.to_excel(writer, sheet_name='time_allocations', index=False, startrow=row_index)
        subject_summary_titles = ['Person', '12 Month Budget', 'Total Hours/Subject', 'Per Subject Effort']
        for col_num, value in enumerate(subject_summary_df.columns.values):
            worksheet_time.write(row_index, col_num, subject_summary_titles[col_num], header_format)
        row_index += subject_summary_df.shape[0] + 2

        # Total summary
        summary_name = pd.DataFrame(columns=['Total Effort Values'])
        summary_name.to_excel(writer, sheet_name='time_allocations', index=False, startrow=row_index)
        worksheet_time.write(row_index, 0, summary_name.columns.values[0], header_format)
        row_index += 1
        total_summary_df = get_total_summary_df(id, subject_summary_df, people, arms)
        total_summary_df.to_excel(writer, sheet_name='time_allocations', index=False, startrow=row_index)
        total_summary_titles = ['Person', 'Total Hours Budgeted Subjects', 'Addl. Lump Sum Hours', 'Addl. Lump Sum Effort', 'Total Effort', 'Total Effort MIRIS Personnel Screen']
        for col_num, value in enumerate(total_summary_df.columns.values):
            worksheet_time.write(row_index, col_num, total_summary_titles[col_num], header_format)
        row_index += total_summary_df.shape[0] + 2

        # Complexity
        df_complexity = get_complexity_df(id)
        df_complexity.to_excel(writer, sheet_name='complexity', index=False)
        # Complexity Format
        worksheet_complexity = writer.sheets['complexity']
        complexity_titles = ['Element', 'No Effect (0pts)', 'Min Effect (1pts)', 'Moderate Effect (2pts)', 'Max Effect (3pts)', 'Raw Score', 'Weight', 'Weighted Score']
        complexity_widths = [36, 24, 24, 24, 24, 20, 20, 20]
        for col_num, value in enumerate(df_complexity.columns.values):
            worksheet_complexity.set_column(col_num, col_num, complexity_widths[col_num], body_format)
            worksheet_complexity.write(0, col_num, complexity_titles[col_num], header_format)

        # Summary
        # Total FTE
        row_index = 0
        df_fte = get_summary_fte_df(total_summary_df, df_complexity, people)
        df_fte.to_excel(writer, sheet_name='summary', index=False, startrow=row_index)
        # Total FTE Format
        worksheet_summary = writer.sheets['summary']
        total_fte_titles = ['Person', 'Low Range', 'Complexity Adjustment', 'High Range']
        total_fte_widths = [36, 20, 20, 20]
        for col_num, value in enumerate(df_fte.columns.values):
            worksheet_summary.set_column(col_num, col_num, total_fte_widths[col_num], body_format)
            worksheet_summary.write(row_index, col_num, total_fte_titles[col_num], header_format)
        row_index += df_fte.shape[0] + 2

        # FTE by person by arm
        # Add arm headers
        arm_cols = ['Arm']
        for arm in arms:
            arm_cols.append(arm.name)
        arms_df = pd.DataFrame(columns=arm_cols)
        arms_df.to_excel(writer, sheet_name='time_allocations', index=False, startrow=row_index)
        for col_num, value in enumerate(arms_df.columns.values):
            worksheet_time.write(row_index, col_num, value, header_format)
        row_index += 1
        df_fte_person_arm = get_person_arm_fte_df(person_arm_hours_df, people, arms)
        df_fte_person_arm.to_excel(writer, sheet_name='summary', index=False, startrow=row_index)
        for col_num, value in enumerate(df_fte_person_arm.columns.values):
            if col_num == 0:
                width = 36
            else:
                width = 20
            worksheet_summary.set_column(col_num, col_num, width, body_format)
            worksheet_summary.write(row_index, col_num, value, header_format)
        row_index += df_fte_person_arm.shape[0] + 2

        # Format
        workbook = writer.book

        # Add some cell formats.
        cell_format = workbook.add_format()
        cell_format.set_font_size(14)

        writer.save()


    # Get media root for download
    mediapath = settings.MEDIA_URL + 'exports/' + filepath.split('/')[-1]

    return mediapath
