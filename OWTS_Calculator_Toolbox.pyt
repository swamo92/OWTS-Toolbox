# The below toolbox is designed to facilitate and expedite the calculation of basic statistics for input data in a specified area
# of interest. Specifically it is intended for calculating the number of Onsite Wastewater Treatment Systems (OWTS)
# in sensitive watersheds. In my application I used it for calculating the number of sub-standard septic systems in the
# Special Area Management Plan (SAMP) watershed in Charlestown, RI. This tool was developed by Seaver Anderson and
# is licensed under the MIT License found in the LICENSE.md file in the repository.

import arcpy

# Create the toolbox
class Toolbox(object):
    def __init__(self):
        """Toolbox name = OWTSCalculator"""
        self.label = "OWTSCalculator"
        self.alias = "SAMP OWTS Calculator"

        # Names of tools found in the toolbox.
        self.tools = [Select, Clip, Statistics]


# Select Tool used to select the OWTS type you would like to run statistics on. For best analysis results select a
# septic system type from the 'Septic_Sys' field.

class Select(object):
    def __init__(self):
        # Tool name and description.
        self.label = "Select"
        self.description = "Selects queried data from input Onsite Wastewater Treatment System (OWTS) layer"
        self.canRunInBackground = False

        # Parameters used to run the tool.

    def getParameterInfo(self):
        parameters = []
        input_point = arcpy.Parameter(name="input_point",
                                      # Parameter 0: input layer you would like to perform analysis on.
                                      displayName="Input Point",
                                      datatype="DEFeatureClass",
                                      parameterType="Required",  # Required parameter
                                      direction="Input",  # Input|Output
                                      )
        parameters.append(input_point)

        output_point = arcpy.Parameter(name="output_point",  # Parameter 1: define output of selected features.
                                       displayName="Output Point",
                                       datatype="DEFeatureClass",
                                       parameterType="Required",  # Required parameter
                                       direction="Output",  # Input|Output
                                       )
        parameters.append(output_point)

        where_clause = arcpy.Parameter(name="where_clause",  # Parameter 2: SQL statement used to select desired data.
                                       displayName="SQL Expression",
                                       datatype="GPSQLExpression",
                                       parameterType="Required",  # Required parameter
                                       direction="Output",  # Input|Output
                                       )
        # Parameter dependencies reference the input feature attribute table to facilitate SQL statement writing.
        where_clause.parameterDependencies = [input_point.name]
        parameters.append(where_clause)

        return parameters

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):  # Script that executes the tool with input parameters.
        in_features = parameters[0].valueAsText
        out_features = parameters[1].valueAsText
        where_clause = parameters[2].valueAsText
        arcpy.Select_analysis(in_features, out_features, where_clause)
        return


# Clip Tool used to clip selected data to the area of interest.

class Clip(object):
    def __init__(self):
        # Tool name and description.
        self.label = "Clip"
        self.description = "Clips the selected data to the Charlestown Special Area Management Plan (SAMP) boundary"
        self.canRunInBackground = False

    def getParameterInfo(self):
        parameters = []
        input_points = arcpy.Parameter(name="input_points",  # Input shapefile to clip.
                                       displayName="Input Feature",
                                       datatype="DEFeatureClass",
                                       parameterType="Required",  # Required parameter.
                                       direction="Input", )  # Input|Output

        parameters.append(input_points)

        input_extent = arcpy.Parameter(name="extent",  # Feature to clip input shapefile to.
                                       displayName="Clip Extent",
                                       datatype="DEFeatureClass",
                                       parameterType="Required",  # Required parameter.
                                       direction="Input")  # Input|Output

        parameters.append(input_extent)

        output = arcpy.Parameter(name="output",  # Output for clipped shapefile.
                                 displayName="Output Shapefile",
                                 datatype="DEFeatureClass",
                                 parameterType="Required",  # Required parameter.
                                 direction="Output")  # Input|Output
        parameters.append(output)

        return parameters

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):  # Execute clip tool.
        in_points = parameters[0].valueAsText
        extent = parameters[1].valueAsText
        output = parameters[2].valueAsText
        arcpy.Clip_analysis(in_points, extent, output)
        return


# Statistics Tool used to calculate statistics for OWTS' in the clipped area of interest.
# For intended results run COUNT statistics on the 'Septic_Sys' field to find the number of
# specified systems (i.e. Advanced or Sub-standard) the SAMP. 

class Statistics(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Statistics"
        self.description = "Calculates statistics for Onsite Wastewater Systems in the Charlestown SAMP"
        self.canRunInBackground = False

    def getParameterInfo(self):
        parameters = []
        input_table = arcpy.Parameter(name="input_data",  # Input table to run stats on.
                                      displayName="Input Data",
                                      datatype="DETable",
                                      parameterType="Required",  # Required parameter.
                                      direction="Input", )  # Input|Output

        parameters.append(input_table)

        output_table = arcpy.Parameter(name="output_table",  # Output table name and destination.
                                       displayName="Output Table",
                                       datatype="DETable",
                                       parameterType="Required",  # Required parameter.
                                       direction="Output")  # Input|Output

        parameters.append(output_table)

        statistics_field = arcpy.Parameter(name="statistics_field",  # Define desired statistics of clipped shapefile.
                                           displayName="Statistics Field",
                                           datatype="GPValueTable",
                                           parameterType="Required",  # Required parameter.
                                           direction="Input")  # Input|Output
        # Parameter dependencies used to reference input data and provide calculable statistics.
        statistics_field.parameterDependencies = [input_table.name]
        statistics_field.columns = [['Field', 'Field'], ['String', 'Statistic Type']]
        statistics_field.filters[1].type = 'ValueList'
        statistics_field.values = [['NAME', 'SUM']]
        statistics_field.filters[1].list = ['COUNT', 'SUM', 'MEAN', 'MAX']
        parameters.append(statistics_field)

        return parameters

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):  # Execute statistics tool.
        in_table = parameters[0].valueAsText
        out_table = parameters[1].valueAsText
        statistics = parameters[2].valueAsText
        arcpy.Statistics_analysis(in_table, out_table, statistics)
        return
