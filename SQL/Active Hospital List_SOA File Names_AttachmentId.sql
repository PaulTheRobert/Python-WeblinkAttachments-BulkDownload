/*
	Created By: Paul Davis
	Created on: 03042021

	Purpose: Preliminary review of SOA files to be downoaded for all OPOs from iTx.
*/

SELECT
	  AFO.[Id]
	, ORG.[OwnedByOrganizationName]
	, AFO.[SourceFileName]
	, ORG.[OrganizationName] 

	, AFO.*

FROM
	[iTxRepl].[dbo].[AttachmentForOrganization] AFO

	INNER JOIN [DCIDSDW].[Dim].[Organization] ORG ON ORG.[OrganizationId] = AFO.[OrganizationId]

WHERE
	ORG.[IsActive] = 'Yes'
	AND ORG.[IsHospital] = 'Yes'
	AND

	(
		AFO.[SourceFileName] LIKE '%SOA%'
		OR AFO.[Description] LIKE '%SOA%'
		OR AFO.[SourceFileName] LIKE '%Agreement%'
		AND AFO.[SourceFileName] NOT LIKE '%TX%'
	)


ORDER BY
	ORG.[OwnedByOrganizationName]
	, ORG.[OrganizationName]


--SELECT AFO.[Id], ORG.[OwnedByOrganizationName], AFO.[SourceFileName], ORG.[OrganizationName] FROM [iTxRepl].[dbo].[AttachmentForOrganization] AFO INNER JOIN [DCIDSDW].[Dim].[Organization] ORG ON ORG.[OrganizationId] = AFO.[OrganizationId] WHERE 	ORG.[IsActive] = 'Yes' 	AND ORG.[IsHospital] = 'Yes' AND (AFO.[SourceFileName] LIKE '%SOA%'		OR AFO.[Description] LIKE '%SOA%'		OR AFO.[SourceFileName] LIKE '%Agreement%'		AND AFO.[SourceFileName] NOT LIKE '%TX%') ORDER BY 	ORG.[OwnedByOrganizationName] 	, ORG.[OrganizationName]