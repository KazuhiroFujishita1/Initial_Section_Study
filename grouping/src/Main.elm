module Main exposing (..)


import Html exposing (..)
import Html.Attributes as Attr
import Html.Events exposing (..)

import Browser
import Browser.Navigation as Nav
import Url
import Url.Parser exposing (Parser)

import Svg exposing (Svg)
import Svg.Attributes as SvgAttr
import Html.Attributes exposing (class)

import Dict exposing (Dict)
import List.Extra exposing (uniqueBy)
import Dict exposing (update)


type alias Position = 
    { x : Int 
    , y : Int 
    }


type alias Member = 
    { start : Position 
    , end : Position 
    , mark : Int 
    , indicator : Indicator
    }

type Updated 
    = Same
    | Up
    | Down 

type alias Section = 
    { no : Int
    , depth : Float 
    , updated : Updated
    }

type alias Indicator = 
    { safeRatio : Float 
    }

type alias Plan = 
    { xAxisCount : Int
    , yAxisCount : Int 
    }

type alias Model = 
    { plan : Plan 
    , members : List Member
    , sections : List Section
    }


type Constraint 
    = Range (Int, Int)
    | AllRange 
    | Impossible

limitDepth : Int
limitDepth = 10000

buildConstraint : Int -> List Constraint
buildConstraint depth  =
    [ Range (depth, depth)
    , Range (0, depth - 200)
    , Range (depth + 200, limitDepth)
    ]

checkConstraint : Float -> Constraint -> Bool
checkConstraint depth const = 
    case const of 
        AllRange -> True
        Impossible -> False
        Range (lower, upper) -> 
            let 
                depthRounded = round depth
            in
            lower <= depthRounded && depthRounded <= upper

mergeConstraint : Constraint -> Constraint -> Constraint
mergeConstraint c1 c2 = 
    case (c1, c2) of
        (Range (l1, u1), Range (l2, u2)) -> 
            let
                maxLower = max l1 l2
                minUpper = min u1 u2
            in

            -- 領域が重なっていなければ両者を満足させる制約は存在しない
            if 0 < (l2 - u1) || 0 < (l1 - u2) then
                Impossible
            else
                Range (maxLower, minUpper)
        (AllRange, AllRange) -> AllRange
        (AllRange, Range (l, u)) -> Range (l, u)
        (Range (l, u), AllRange) -> Range (l, u)
        (Impossible, _) -> Impossible 
        (_, Impossible) -> Impossible

mergeConstraints : List Constraint -> List Constraint -> List Constraint
mergeConstraints src dst =
    dst
    |> List.concatMap (\c1 ->
        src
        |> List.map (\c2 ->
            mergeConstraint c1 c2     
        )
    )
    |> List.filter (\c -> 
        case c of 
            Impossible -> False
            _ -> True 
    )

defaultIndicator : Indicator 
defaultIndicator = { safeRatio = 0.5 }
generateMembers : (Int -> Position) -> List Int -> List Member 
generateMembers intToPos markList = 
    markList
    |> List.indexedMap (\index mark -> 
        let 
            startPos = index + 1
            endPos   = index + 2
        in
        if mark == 0 then
            Nothing
        else
            Just 
                { mark = mark 
                , start = intToPos startPos
                , end = intToPos endPos
                , indicator = defaultIndicator  
                } 
    )
    |> List.filterMap (\x -> x)



defaultModel : Model
defaultModel = 
    let
        xFrames = 
            [ [ 2, 1, 2, 0 ]  
            , [ 3, 1, 3, 4 ]  
            , [ 3, 1, 3, 4 ]  
            , [ 2, 1, 2, 0 ]  
            ]
        yFrames = 
            [ [ 12, 11, 12 ]  
            , [ 13, 11, 13 ]  
            , [ 13, 11, 13 ]  
            , [ 12, 11, 12 ]  
            , [  0, 14,  0 ]  
            ]
        
        xMembers = 
            xFrames
            |> List.indexedMap (\index marks ->
                let

                    intToPos : Int -> Position 
                    intToPos = \axisIndex -> { x = axisIndex, y = index + 1 }
                in
                generateMembers intToPos marks
            )
            |> List.concat

        yMembers = 
            yFrames
            |> List.indexedMap (\index marks ->
                let

                    intToPos : Int -> Position 
                    intToPos = \axisIndex -> { x = index + 1, y = axisIndex }
                in
                generateMembers intToPos marks
            )
            |> List.concat

        members = List.concat [ xMembers, yMembers ]

        sections = 
            [ { no =  1, depth =  500.0, updated = Same }  
            , { no =  2, depth =  700.0, updated = Same }  
            , { no =  3, depth =  600.0, updated = Same }  
            , { no =  4, depth =  400.0, updated = Same }  
            , { no = 11, depth =  800.0, updated = Same }  
            , { no = 12, depth = 1000.0, updated = Same }  
            , { no = 13, depth =  900.0, updated = Same }  
            , { no = 14, depth =  400.0, updated = Same }  
            ]

    in
    { plan = { xAxisCount = 5, yAxisCount = 4 } 
    , members = members
    , sections = sections
    }
    |> Debug.log "default model"

type Msg 
    = None
    | SetIndicator (Position, Position, Indicator)
    | SetDepth (Position, Position, Float) 




main : Program () Model Msg
main =
  Browser.application
    { init = init
    , view = view
    , update = update
    , subscriptions = subscriptions
    , onUrlChange = \_ -> None
    , onUrlRequest = \_ -> None 
    }

init : () -> Url.Url -> Nav.Key -> (Model, Cmd Msg)
init () url key =
    (defaultModel, Cmd.none) 


subscriptions : Model -> Sub Msg
subscriptions _ =
    Sub.none

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of 
        _ -> (model, Cmd.none) 

margin : Float
margin = 20.0

canvasWidth : Float
canvasWidth = 600.0

canvasHeight : Float
canvasHeight = 500.0

colors : List String
colors = 
    [ "orange"
    , "blue"
    , "green"
    , "purple"
    , "gray"
    , "navy"
    , "olive"
    , "lime"
    , "maroon"
    , "silver"
    , "teal"
    , "yellow"
    ]

isDiffUnder100 : Section -> Section -> Bool
isDiffUnder100 s1 s2 = 
    abs (s1.depth - s2.depth) <= 100.0

isDiff100To200 : Section -> Section -> Bool
isDiff100To200 s1 s2 = 
    100.0 < abs (s1.depth - s2.depth)  &&
            abs (s1.depth - s2.depth) < 200.0


getJointMessage : Section -> Section -> String 
getJointMessage s1 s2 = 
    if isDiffUnder100 s1 s2 then
        "~100"
    else if isDiff100To200 s1 s2 then
        "100~200"
    else
        ""

checkDiaphragm : Section -> Section -> Bool
checkDiaphragm s1 s2 =
    let
        diff = abs (s1.depth - s2.depth)
    in
    diff == 0.0 || 200.0 <= diff


-- 当該断面Noのメンバーを取得する
sectionMembers : Model -> Int -> List Member
sectionMembers model no =
    model.members
    |> List.filter (\m -> m.mark == no)


-- 当該箇所に所属するメンバーを取得
jointMembers : Model -> Position -> List Member
jointMembers model position = 
    model.members
    |> List.filter (\m ->
        m.start == position || m.end == position
    )


-- 当該メンバーに接続するメンバー一覧を取得
connectedMembers : Model -> Member -> List Member
connectedMembers model target =
    model.members
    |> List.filter (\m -> m /= target)
    |> List.filter (\m -> 
        m.start == target.start || m.end == target.end ||
        m.start == target.end   || m.end == target.start 
    )

-- 当該メンバーに接続する断面符号一覧を取得
connectedSectionMarks : Model -> Member -> List Int
connectedSectionMarks model member =
    connectedMembers model member 
    |> List.map (\m -> m.mark)
    |> uniqueBy (\mark -> mark)

-- 指定位置のダイアフラムが要件を満たさない場合はTrue
checkNotSatisfiedDiaphragmOnPosition : Model -> Position -> Bool
checkNotSatisfiedDiaphragmOnPosition model position = 
    let
        members = jointMembers model position
        sectionNos =  
            members 
            |> uniqueBy (\m -> m.mark)
            |> List.map (\m -> m.mark)

        sectionMap = 
            model.sections
            |> List.map (\s -> (s.no, s))
            |> Dict.fromList 

        sectionNoPairs = 
            sectionNos
            |> List.map (\no ->
                (no, sectionNos |> List.filter (\secNo -> secNo /= no))
            )
    in
    sectionNoPairs
    |> List.concatMap (\(no, otherNos) ->
        otherNos |> List.map (\otherNo -> (no, otherNo))
    )
    |> List.filterMap (\(n1, n2) ->
        let
            s1 = sectionMap |> Dict.get n1
            s2 = sectionMap |> Dict.get n2
        in
        case (s1, s2) of
            (Just section1, Just section2) -> Just (checkDiaphragm section1 section2)
            (_, _) -> Nothing
    )
    |> List.all (\x -> x)
    |> not

checkNotSatisfiedDiaphragmRelatedMember : Model -> Member -> Bool
checkNotSatisfiedDiaphragmRelatedMember model member = 
    checkNotSatisfiedDiaphragmOnPosition model member.start ||
    checkNotSatisfiedDiaphragmOnPosition model member.end 


positions : Model -> List Position
positions model = 
    List.range 1 model.plan.yAxisCount
    |> List.concatMap (\xIndex ->
        List.range 1 model.plan.xAxisCount
        |> List.map (\yIndex ->
            { x = xIndex, y = yIndex }
        )
    )

getCoord : Model -> Position -> (Float, Float)
getCoord model position = 
    let
        xInterval = (canvasWidth - 2.0 * margin) / 
                    (toFloat (model.plan.xAxisCount - 1)) 
        yInterval = (canvasHeight - 2.0 * margin) / 
                    (toFloat (model.plan.yAxisCount - 1)) 

        x = margin + xInterval * (toFloat (position.x - 1))
             
        y = -1.0 * (margin + yInterval * (toFloat (position.y - 1)))
    in
    (x, y)


buildSectionConstraints : Model -> Section -> List Constraint 
buildSectionConstraints model section = 
    let
        sectionMap : Dict Int Section
        sectionMap =
            model.sections
            |> List.map (\s -> (s.no, s)) 
            |> Dict.fromList

        members = sectionMembers model section.no

        selfSectionNo = section.no 

        targetSectionNos = 
            members
            |> List.concatMap (\m -> 
                connectedSectionMarks model m  
            )
            |> List.filter (\no -> no /= selfSectionNo)
            |> uniqueBy (\no -> no)

        targetDepths =  
            targetSectionNos
            |> List.filterMap (\no -> Dict.get no sectionMap)
            |> uniqueBy (\no -> no)
            |> List.map (\s -> round s.depth)

        constraints =
            targetDepths
            |> List.map buildConstraint
            |> List.foldl (mergeConstraints) [ AllRange ]
    in
    constraints 

type alias SolvedConstraintResult = 
    { isSatisfied : Bool
    , section : Section 
    , candidates : List Float
    }

solveSectionConstraints : Section -> List Constraint -> SolvedConstraintResult 
solveSectionConstraints section constraints = 
    let
        selfDepth = section.depth

        isSatisfied = 
            (
                constraints
                |> List.filter (checkConstraint selfDepth)
                |> List.length
            ) > 0

        (lowerDepth, upperDepth) = 
            constraints
            |> List.foldl (\const (currentLowerDepth, currentUpperDepth) -> 
                case const of
                    Range (lowerRangeInt, upperRangeInt) -> 
                        let
                            lowerRange = toFloat lowerRangeInt
                            upperRange = toFloat upperRangeInt
                        in
                        (
                            if upperRange <= selfDepth then max currentLowerDepth upperRange
                                                       else currentLowerDepth  
                        ,
                            if selfDepth <= lowerRange then min currentUpperDepth lowerRange
                                                       else currentUpperDepth 
                        )
                    _ -> (currentLowerDepth, currentUpperDepth)
            ) (0.0, toFloat limitDepth)
    in
    { isSatisfied = isSatisfied
    , section = section
    , candidates  = if isSatisfied then [ selfDepth ] else ([ lowerDepth, upperDepth ] |> uniqueBy (\x -> x))
    }

{-
    - 符号ごとにOK範囲を結合する
    - 優先度を決めて更新
    - 繰り返す 
-}
solveDiaphragmConstraints : Int -> Model -> Model
solveDiaphragmConstraints count model = 
    let

        _ = count |> Debug.log "count"

    
        --
        sectionConstraints = 
            model.sections
            |> List.map (\section -> (section, buildSectionConstraints model section))


        -- 制約を満たさない断面結果一覧
        unSatisfiedResults =    
            sectionConstraints
            |> List.map (\(section, constraints) -> solveSectionConstraints section constraints)
            |> List.filter (\result -> not result.isSatisfied)
    in
    if List.length (unSatisfiedResults) == 0 || 10 <= count then
        model 
    else
        let
    
            {-
              符号分岐の検討
              実際には各階に波及させる必要があるので
              全層に渡って制約を満たしている箇所であることを判断する必要がある
            -}
            unSatisfiedSecNoMap =
                unSatisfiedResults
                |> List.map (\result -> (result.section.no, result.section))
                |> Dict.fromList 

            copyNewSection : List Section -> Section -> Section  
            copyNewSection orgSections baseSection = 
                let
                    getWithDefault defValue value = 
                        case value of 
                            Just v -> v
                            Nothing -> defValue 
                    maxNo  = orgSections |> List.map (\s -> s.no)
                                         |> List.maximum  
                                         |> getWithDefault 1
                    nextNo = max 100 (maxNo + 1) 
                        -- case (
                        --     List.range 1 maxNo
                        --     |> List.filter (\no -> not (List.any (\section -> section.no == no) orgSections))
                        --     |> List.head
                        -- ) of 
                        --     Just no -> no
                        --     Nothing -> maxNo + 1
                        
                in
                { baseSection | no = nextNo }
                |> Debug.log ("new section " ++ (String.fromInt baseSection.no) ++ " -> " ++ (String.fromInt nextNo) )

            newSectionMap =
                unSatisfiedResults
                |> List.foldl (\result currentPairs -> 
                    let
                        currentSections = currentPairs |> List.map (\(_, section) -> section)

                        newSection = copyNewSection currentSections result.section 
                    in 
                    (result.section.no, newSection) :: currentPairs
                    
                ) 
                (model.sections |> List.map (\section -> (section.no, section)))
                |> List.filter (\(secNo, newSection) -> 
                    case Dict.get secNo unSatisfiedSecNoMap of
                        Just _   -> secNo /= newSection.no 
                        Nothing  -> False
                )
                |> Debug.log "new section map"
                |> Dict.fromList

            enabledMarkChange = True
            --enabledMarkChange = False
            (newMembers, newSections) =
                if enabledMarkChange then 
                    model.members
                    |> List.foldl (\m (members, sections) ->
                        case Dict.get m.mark newSectionMap of
                            Just newSection -> 
                                if checkNotSatisfiedDiaphragmRelatedMember model m 
                                then  (m :: members, sections) 
                                else
                                    let
                                        _ = newSection 
                                            |> Debug.log ("add new mark " ++ (String.fromInt newSection.no))
                                        _ = m |> Debug.log "member"
                                    in
                                    (
                                        { m | mark = newSection.no } :: members,
                                        if List.any (\sec -> sec.no == newSection.no) sections
                                        then sections
                                        else 
                                            newSection :: sections
                                    )
                            Nothing -> 
                                (m :: members, sections)

                    ) ([], model.sections)
                    |> \(ms, ss) -> 
                        (
                            List.reverse ms , 
                            List.reverse ss
                        )
                else
                    (model.members, model.sections) 

            -- 最も差分が小さいものを選択
            targetMaybe =
                unSatisfiedResults
                |> List.concatMap (\result ->
                    result.candidates 
                    |> List.map (\candidateDepth -> (result, candidateDepth))
                )
                |> List.sortBy (\(result, depth) -> abs (depth - result.section.depth))
                |> List.head
            newUpdatedSections =
                case targetMaybe of
                    Nothing -> newSections 
                    Just (targetResult, newDepth) ->
                        newSections
                        |> List.map (\section ->
                            if section.no == targetResult.section.no 
                            then 
                                { section | depth = newDepth
                                , updated = if 0.0 < newDepth - section.depth 
                                            then Up 
                                            else if newDepth - section.depth < 0.0
                                            then Down
                                            else Same
                                }

                            else section
                        )

        in

        -- 再帰
        solveDiaphragmConstraints (count + 1) { model | members = newMembers
                                                      , sections = newUpdatedSections }


    




viewPlan : Model -> List (Svg Msg)
viewPlan model = 
    let
        sectionMap : Dict Int (Section, String)
        sectionMap =
            model.sections
            |> List.sortBy (\sec -> sec.no)
            |> List.indexedMap (\index s -> 
                let
                    color = 
                        case (colors |> List.drop index |> List.head) of
                            Just x -> x
                            Nothing -> "black"    
                        
                in
                (s.no, (s, color))
            ) 
            |> Dict.fromList

        members = 
            model.members
            |> List.concatMap (\member -> 
                let
                    toS = String.fromFloat 
                    start = member.start
                    end = member.end

                    (x1, y1) = getCoord model start
                    (x2, y2) = getCoord model end

                    (section, color) = 
                        case Dict.get member.mark sectionMap of
                            Just (s, c) -> (s, c)
                            Nothing -> ({ no = 0, depth = 0.0, updated = Same }, "black")

                    markPostFix = 
                        case section.updated of
                            Same -> ""
                            Down -> "↓" 
                            Up   -> "↑" 

                    markText =
                        Svg.text_
                            (
                                [ SvgAttr.x (0.5 * (x1 + x2) |> toS)
                                , SvgAttr.y (0.5 * (y1 + y2) |> toS)
                                , SvgAttr.dominantBaseline "text-before-edge"
                                , SvgAttr.textAnchor "middle"
                                , SvgAttr.color color
                                , SvgAttr.stroke color
                                , SvgAttr.fill color
                                ] ++ 
                                (
                                    case section.updated of
                                        Same -> []
                                        _    -> [ SvgAttr.textDecoration "underline" ]
                                ) 
                            )
                            [ text ("G" ++ String.fromInt member.mark ++ markPostFix) ] 

                    depthText = 
                        Svg.text_
                            [ SvgAttr.x (0.5 * (x1 + x2) |> toS)
                            , SvgAttr.y (0.5 * (y1 + y2) |> toS)
                            , SvgAttr.dominantBaseline "text-after-edge"
                            , SvgAttr.textAnchor "middle"
                            , SvgAttr.color color
                            , SvgAttr.stroke color
                            , SvgAttr.fill color
                            ]
                            [ text (String.fromFloat section.depth) ] 



                in
                [ Svg.line
                    [ SvgAttr.x1 (toS x1)
                    , SvgAttr.y1 (toS y1)
                    , SvgAttr.x2 (toS x2)
                    , SvgAttr.y2 (toS y2)
                    , SvgAttr.stroke color 
                    , SvgAttr.strokeWidth "2"
                    ]
                    []
                , markText
                , depthText
                ]
            
            )
        
        jointCheck = 
            positions model
            |> List.filter (checkNotSatisfiedDiaphragmOnPosition model)
            |> List.map (\position ->
                let
                    (x, y) = getCoord model position 
                in
                
                Svg.circle
                    [ SvgAttr.stroke "red" 
                    , SvgAttr.strokeWidth "1.0" 
                    , SvgAttr.fill "red"
                    , SvgAttr.opacity "0.5"
                    , SvgAttr.cx (String.fromFloat x) 
                    , SvgAttr.cy (String.fromFloat y)
                    , SvgAttr.r "8px" 
                    ]
                    []
            )
            

        svgContents = 
            [ members
            , jointCheck 
            ]
            |> List.concat

    in
    svgContents 


view : Model -> Browser.Document Msg
view model = 
    let 
        width = String.fromFloat canvasWidth
        height = String.fromFloat canvasHeight
        x = String.fromFloat 0.0
        y = String.fromFloat (-1.0 * canvasHeight)

        svgCanvas contents = 
            Svg.svg 
                [ SvgAttr.width width 
                , SvgAttr.height height 
                , SvgAttr.viewBox ([ x, y, width, height ] |> String.join " ")
                , Attr.style "margin" "0 auto"
                ]
                contents 

        columnStyle =
            [ Attr.style "height" "100vh"
            , Attr.style "width" "100%"
            , Attr.style "text-align" "center"
            , Attr.style "display" "flex"
            , Attr.style "align-items" "flex"
            , Attr.style "justify-content" "center" ]

        leftPane = 
            Html.div 
                ( (class "column" ) :: columnStyle)
                [ svgCanvas 
                    ( 
                        (
                            Svg.rect 
                                [ SvgAttr.x (String.fromFloat 0.0) 
                                , SvgAttr.y (String.fromFloat (-1.0 * canvasHeight)) 
                                , SvgAttr.width (String.fromFloat canvasWidth) 
                                , SvgAttr.height (String.fromFloat canvasHeight) 
                                , SvgAttr.stroke "black"
                                , SvgAttr.fill "transparent"
                                , SvgAttr.strokeWidth "1"
                                ] 
                                []
                        ) :: (viewPlan model) 
                    ) 
                ]
        
        solvedModel = solveDiaphragmConstraints 1 model
        rightPane = 
            Html.div 
                ( (class "column" ) :: columnStyle)
                [ svgCanvas 
                    ( 
                        (
                            Svg.rect 
                                [ SvgAttr.x (String.fromFloat 0.0) 
                                , SvgAttr.y (String.fromFloat (-1.0 * canvasHeight)) 
                                , SvgAttr.width (String.fromFloat canvasWidth) 
                                , SvgAttr.height (String.fromFloat canvasHeight) 
                                , SvgAttr.stroke "black"
                                , SvgAttr.fill "transparent"
                                , SvgAttr.strokeWidth "1"
                                ] 
                                []
                        ) :: (viewPlan solvedModel) 
                    ) 
                ]
        body = 
            Html.div 
                [ Attr.style "display" "flex" ]
                [ leftPane
                , rightPane 
                ]
    in
    { title = ""
    , body = [ body ] 
    }