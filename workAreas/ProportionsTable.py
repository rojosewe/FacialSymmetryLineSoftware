from tkintertable.TableModels import TableModel
from tkintertable.Tables import TableCanvas
from utils.Messages import messages as ms

def humanLengthProps(prop):
    if prop > 1.0:
        d = (prop - 1) * 100
        return ms["left_displacement"].format(d)
    elif prop < 1.0:
        d = (1 - prop) * 100
        return ms["right_displacement"].format(d)
    else:
        return ms["no_displacement"]


def humanAngleProps(prop):
    if prop > 1.0:
        d = (prop - 1) * 100
        return ms["right_angle_displacement"].format(d)
    elif prop < 1.0:
        d = (1 - prop) * 100
        return ms["left_angle_displacement"].format(d)
    else:
        return ms["no_angle_displacement"]


def showProportions(tableFrame, patient, complete, showUpperMeasures, showLowerMeasures, showUpperAngles, showLowerAngles):
    table = TableCanvas(tableFrame)
    table.createTableFrame()
    if complete:
        prop = patient.proportions
    else:
        return
    model = table.model
    data = {ms.get("longitud")}
    model.importDict(data)
    table.redrawTable()


def oldShowProportions(patient, complete, showUpperMeasures, showLowerMeasures, showUpperAngles, showLowerAngles):
    if complete:
        prop = patient.proportions
    else:
        return
    a = {}
    x = [humanLengthProps(prop.internalCantLength), humanLengthProps(prop.externalCantLength),
         humanLengthProps(prop.tragoLength), humanLengthProps(prop.rebordeAlarLength),
         humanLengthProps(prop.lipLength), humanLengthProps(prop.mandibleLength),
         humanAngleProps(prop.glabelarCantoIntAngle), humanAngleProps(prop.glabelarCantoExtAngle),
         humanAngleProps(prop.glablearTragoAngle), humanAngleProps(prop.glablearNasalAngle),
         humanLengthProps(prop.glablearLabialAngle), humanLengthProps(prop.glablearMadibularAngle),
         humanAngleProps(prop.pogonionTragoAngle), humanLengthProps(prop.pogonionLabialAngle),
         humanLengthProps(prop.pogonionMandibularAngle), humanLengthProps(prop.lengthAverage),
         humanLengthProps(prop.upperLengthAverage), humanLengthProps(prop.lowerLengthAverage),
         humanAngleProps(prop.angleAverage), humanAngleProps(prop.lowerAngleAverage),
         humanAngleProps(prop.upperAngleAverage)]
    for i in range(len(x)):
        a["a_" + str(i)] = x[i]
    z = ms.copy()
    z.update(a)
    msg = "{measurements_props}:".format_map(z)
    if showUpperMeasures:
        msg += """
    - {internal_cant}: {a_0}
    - {external_cant}: {a_1}
    - {trago}: {a_2}
    - {reborde_alar}: {a_3}""".format_map(z)
    if showLowerMeasures:
        msg += """
    - {mouth}: {a_4}
    - {mandibular_angle}: {a_5}
    """.format_map(z)
    if showUpperMeasures and showLowerMeasures:
        msg += """
    {total_length_move}: {a_15}
    ------------------------------------------------------
    """.format_map(z)
    elif showUpperMeasures:
        msg += """
    {total_length_move}: {a_16}
    ------------------------------------------------------
    """.format_map(z)
    elif showLowerMeasures:
        msg += """
    {total_length_move}: {a_17}
    ------------------------------------------------------
    """.format_map(z)

    msg += """
    {angular_proportions}:    
        """.format_map(z)
    if showUpperAngles:
        msg += """
    - {glabelar} - {internal_cant}: {a_6}
    - {glabelar} - {external_cant}: {a_7}
    - {glabelar} - {trago}: {a_8}
    - {glabelar} - {reborde_alar}: {a_9}""".format_map(z)
    if showLowerAngles:
        msg += """
    - {glabelar} - {mouth}: {a_10}
    - {glabelar} - {mandibular_angle}: {a_11}
    - {pogonion} - {trago}: {a_12}
    - {pogonion} - {mouth}: {a_13}
    - {pogonion} - {mandibular_angle}: {a_14}
    """.format_map(z)
    if showUpperAngles and showLowerAngles:
        msg += """
    {total_angle_move}: {a_18}
    """.format_map(z)
    elif showUpperAngles:
        msg += """
    {total_angle_move}: {a_19}
    """.format_map(z)
    elif showLowerAngles:
        msg += """
    {total_angle_move}: {a_20}
    """.format_map(z)